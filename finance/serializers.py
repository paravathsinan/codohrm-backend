from rest_framework import serializers
from .models import Reimbursement

class ReimbursementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reimbursement
        fields = ('id', 'transaction_date', 'amount', 'purpose', 'supporting_doc_url', 'status')
