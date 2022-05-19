from rest_framework.views import APIView
from customadmin.models import PhoneNumberCode, UserPhoneNumber, PersonalChart, FoundationCode, SocialCode, FamilyCode, OtherCode, NumberCode
from numerology.helpers import custom_response, serialized_response
from rest_framework import status
from django.db.models import Q
from ..serializers import PersonalChartSerializer
from datetime import datetime


def get_sum(num):
    while int(num) > 9:
        num = sum(map(int, str(num)))
    return int(num)

    


class PhoneNumberChartAPIView(APIView):
    """
    Phone Number chart View
    """

    def post(self, request):
        phone_number = request.data['phone_number']
        if not phone_number:
            message = "Phone Number is required!"
            return custom_response(True, status.HTTP_200_OK, message)

        if len(phone_number)!=8:
            message = "Invalid Phone Number!"
            return custom_response(True, status.HTTP_200_OK, message)

        codes = []
        for i in range(0, len(phone_number)-1, 2):
            codes.append(f"{phone_number[i: i+2]}")

        if not UserPhoneNumber.objects.filter(phone=phone_number):
            UserPhoneNumber.objects.create(phone=phone_number)

        phone_number= phone_number[:-1]
        phone_number= phone_number[1:]

        for i in range(0, len(phone_number)-1, 2):
            codes.append(f"{phone_number[i: i+2]}")

        phone_number_codes=[]
        for code in codes:
            codesets = PhoneNumberCode.objects.filter(code=code).first()
            phone_number_codes.append(codesets)

        message = "Phone Number Chart created Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, phone_number_codes)


class PersonalDetailChartAPIView(APIView):
    """
    Personal Detail chart View
    """
    serializer_class = PersonalChartSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        message = "Chart created Successfully!"
        response_status, result, message = serialized_response(serializer, message)

        if not response_status:
            return custom_response(response_status, status.HTTP_400_BAD_REQUEST, message, result)
        personal_chart = {}
        chart_matrix = []
        date_of_birth = request.data['date_of_birth'].split('-')
        formated_dob = date_of_birth[2] + date_of_birth[1] + date_of_birth[0]
        # Line 1
        line1 = [int(i) for i in formated_dob]
        personal_chart['line1']=line1
        # Line 2
        line2 = [get_sum(str(line1[i]) + str(line1[i+1])) for i in range(0, len(line1), 2)]
        personal_chart['line2']=line2
        # line 3
        line3 = [get_sum(str(line2[i]) + str(line2[i+1])) for i in range(0, len(line2), 2)]
        personal_chart['line3']=line3
        # line 4
        line4 = [get_sum(line3[0]+line2[0]), get_sum(line3[0]+line2[1]), get_sum(line2[1]+line2[2]), get_sum(line3[1]+line2[2]), get_sum(line3[1]+line2[3])]
        personal_chart['line4']=line4
        # line 5
        line5 = [get_sum(line4[0]+line4[1]),  get_sum(line3[1]+line4[2]), get_sum(line3[0]+line4[2]), get_sum(line4[3]+line4[4])]
        personal_chart['line5']=line5
        # line 6
        line6 = [get_sum(line5[1]+line5[2])]
        personal_chart['line6']=line6

        # Code generation

        personal_chart['family_code'] = f"{line4[0]}{line4[1]}/{line5[0]}"
        family_code = FamilyCode.objects.filter(code=personal_chart['family_code'])
        personal_chart['family_code_meaning'] = family_code[0].meaning if family_code else ""

        personal_chart['foundation_code'] = f"{line5[1]}{line5[2]}/{line6[0]}"
        foundation_code = FoundationCode.objects.filter(code=personal_chart['foundation_code'])
        personal_chart['foundation_code_meaning'] = foundation_code[0].meaning if foundation_code else ""

        personal_chart['social_code'] = f"{line4[3]}{line4[4]}/{line5[3]}"
        social_code = SocialCode.objects.filter(code=personal_chart['social_code'])
        personal_chart['social_code_meaning'] = social_code[0].meaning if social_code else ""

        # Number Code
        code_set= NumberCode.objects.filter(code=line6[0])
        personal_chart['number_code'] = [code.meaning for code in code_set]        
        
        # Other codes
        other_codes = []
        code1 = f"{line1[0]}{line1[1]}/{line2[0]}"
        code1_meaning = OtherCode.objects.filter(code=code1)
        if code1_meaning:
            other_codes.append(code1_meaning[0].meaning)

        code2 = f"{line1[2]}{line1[3]}/{line2[1]}"
        code2_meaning = OtherCode.objects.filter(code=code2)
        if code2_meaning:
            other_codes.append(code2_meaning[0].meaning)

        code3 = f"{line1[4]}{line1[5]}/{line2[2]}"
        code3_meaning = OtherCode.objects.filter(code=code3)
        if code3_meaning:
            other_codes.append(code3_meaning[0].meaning)

        code4 = f"{line1[6]}{line1[7]}/{line2[3]}"
        code4_meaning = OtherCode.objects.filter(code=code4)
        if code4_meaning:
            other_codes.append(code4_meaning[0].meaning)
        
        code5 = f"{line3[0]}{line3[1]}/{line4[2]}"
        code5_meaning = OtherCode.objects.filter(code=code5)
        if code5_meaning:
            other_codes.append(code5_meaning[0].meaning)

        personal_chart['other_codes'] = other_codes
        personal_chart['date_of_birth'] = request.data['date_of_birth']
        personal_chart['name'] = request.data['name']
        message = "Chart created Successfully!"
        return custom_response(True, status.HTTP_200_OK, message, personal_chart)