# coding=utf-8
import datetime
import io

import xlsxwriter
from django.db.models import Sum, F, Count
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.core.utils import digit3
from apps.store.models import Order, OrderItem, FINISHED, ACTIVE, CANCELED, WAITING
from apps.store.serializers import OrderSerializer, OrderItemSerializer
from apps.user.permission import UserIsAdmin


class OrderViewSet(ModelViewSet):
    permission_classes = (UserIsAdmin,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        if self.action == 'retrieve':
            return self.queryset
        else:
            return self.queryset.filter(status=WAITING)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = CANCELED
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        order = self.get_object()
        items = order.orderitem_set.all()
        columns = ['Id', 'Type', 'Name', 'Price', 'Amount', 'Total', 'Status']
        width = len(columns)
        cur_time = datetime.datetime.now()

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        name = workbook.add_format({'bold': True, 'border': 1, 'align': 'center'})
        title = workbook.add_format({'bold': True, 'border': 1})
        meta = workbook.add_format({'border': 1})
        data0 = workbook.add_format({'left': 1, 'right': 1})
        data1 = workbook.add_format({'left': 1, 'right': 1, 'bg_color': '#f2f2f2'})
        data = data1
        end = workbook.add_format({'top': 1})

        row_num = 0

        # Title
        worksheet.merge_range(row_num, 0, row_num, width - 1, 'Order Info', name)
        row_num += 1
        worksheet.merge_range(row_num, 0, row_num, 1, 'Order ID:', title)
        worksheet.merge_range(row_num, 2, row_num, width - 1,
                              str(order.id), meta)
        row_num += 1
        worksheet.merge_range(row_num, 0, row_num, 1, 'Client:', title)
        worksheet.merge_range(row_num, 2, row_num, width - 1,
                              '%s %s(%s)' % (order.client.first_name, order.client.last_name, order.client.username),
                              meta)
        row_num += 1
        worksheet.merge_range(row_num, 0, row_num, 1, 'Address:', title)
        worksheet.merge_range(row_num, 2, row_num, width - 1, order.client.address, meta)
        row_num += 1
        worksheet.merge_range(row_num, 0, row_num, 1, 'Register Time:', title)
        worksheet.merge_range(row_num, 2, row_num, width - 1,
                              order.client.created.strftime('%d-%m-%Y %H:%M:%S'), meta)
        row_num += 1
        worksheet.merge_range(row_num, 0, row_num, 1, 'Print Time:', title)
        worksheet.merge_range(row_num, 2, row_num, width - 1, cur_time.strftime('%d-%m-%Y %H:%M:%S')
                              , meta)
        row_num += 1

        # Table
        for col_num in range(width):
            worksheet.write(row_num, col_num, columns[col_num], title)
        row_num += 1
        for item in items:
            worksheet.write(row_num, 0, item.product.id, data)
            worksheet.write(row_num, 1, item.product.name, data)
            worksheet.write(row_num, 2, item.product.type.name, data)
            worksheet.write(row_num, 3, item.price, data)
            worksheet.write(row_num, 4, item.amount, data)
            worksheet.write(row_num, 5, item.price * item.amount, data)
            worksheet.write(row_num, 6, '✔' if item.status else '', data)

            row_num += 1
            data = data0 if data == data1 else data1

        # End
        info = items.filter(status=True).aggregate(
            money=Sum(F('amount') * F('price')),
            count=Count('amount'))
        money = info['money'] if info['money'] else 0
        count = info['count'] if info['count'] else 0
        infoAll = items.aggregate(
            money=Sum(F('amount') * F('price')),
            count=Count('amount'))
        moneyAll = infoAll['money'] if infoAll['money'] else 0
        countAll = infoAll['count'] if infoAll['count'] else 0

        worksheet.merge_range(row_num, 0, row_num, 1, 'Total:', title)
        if order.status in [ACTIVE, FINISHED]:
            worksheet.merge_range(row_num, 2, row_num, width - 1,
                                  digit3(money)
                                  , title)
        else:
            worksheet.merge_range(row_num, 2, row_num, width - 1,
                                  '%s(%s) / %s(%s)' % (count, digit3(money), countAll, digit3(moneyAll))
                                  , meta)
        row_num += 1

        workbook.close()
        output.seek(0)
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename=%s_%s(%s).xls' % (
            order.client, order.id, cur_time.strftime('%d-%m#%H!%M!%S'))

        return response


class OrderItemViewSet(ModelViewSet):
    permission_classes = (UserIsAdmin,)
    serializer_class = OrderItemSerializer
    queryset = OrderItem.objects.all()
    filter_fields = ('order',)
