from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from customadmin.models import UserPhoneNumber, PhoneNumberCode, NumberCode, FamilyCode, FoundationCode, SocialCode, OtherCode, User
import datetime
import numpy as np
from numerology.helpers import get_cart_count


def get_sum(num):
    while int(num) > 9:
        num = sum(map(int, str(num)))
    return int(num)

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


class FreeChartPageView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)   
        return render(request,"user/phone-number-tab.html",{'page_title': 'Free Charts', 'cart_count': cart_count})


class PhoneNumberChartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        phone_number = request.GET.get('phone')

        if not phone_number:
            return render(request,"user/phone-number-chart.html",{'page_title': 'Phone Number Chart', 'status': False})

        if len(phone_number)!=8:
            return render(request,"user/phone-number-chart.html",{'page_title': 'Phone Number Chart', 'status': False})

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
        return render(request,"user/phone-number-chart.html",{'page_title': 'Phone Number Chart', 'status':True, 'phone_number_codes': phone_number_codes, 'cart_count': cart_count})


class PersonalChartTabPage(View):
    def get(self, request):
        cart_count = get_cart_count(request.user) if request.user.is_authenticated else 0
        return render(request,"user/personal-tab.html",{'page_title': 'Free Charts', 'cart_count': cart_count})


class PersonalChartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
        else:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device, is_active=False)
        cart_count = get_cart_count(user)
        personal_chart = {}
        date_of_birth = request.GET.get('dob')
        name = request.GET.get('name')
        if not date_of_birth:
            return render(request,"user/personal-chart.html",{'page_title': 'Free Charts', 'status': False})

        try:
            datetime.datetime.strptime(date_of_birth, '%m/%d/%Y')
        except ValueError:
            return render(request,"user/personal-chart.html",{'page_title': 'Error Charts', 'status': False})
    
        date_of_birth = date_of_birth.split('/')
        formated_dob = date_of_birth[1] + date_of_birth[0] + date_of_birth[2]

        # Line 1
        line1 = [int(i) for i in formated_dob]
        # Line 2
        line2 = [get_sum(str(line1[i]) + str(line1[i+1])) for i in range(0, len(line1), 2)]
        # line 3
        line3 = [get_sum(str(line2[i]) + str(line2[i+1])) for i in range(0, len(line2), 2)]
        # line 4
        line4 = [get_sum(line3[0]+line2[0]), get_sum(line3[0]+line2[1]), get_sum(line3[0]+line3[1]), get_sum(line3[1]+line2[2]), get_sum(line3[1]+line2[3])]
        # line 5
        line5 = [get_sum(line4[0]+line4[1]),  get_sum(line3[1]+line4[2]), get_sum(line3[0]+line4[2]), get_sum(line4[3]+line4[4])]
        # line 6
        line6 = [get_sum(line5[1]+line5[2])]

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
        code_set= NumberCode.objects.filter(code=line4[2])
        number_code = [code.meaning for code in code_set]
        splitted_number_code = list(split(number_code, 3))

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

        return render(request,"user/personal-chart.html",{'page_title': 'Free Charts', 'name': name, 'formated_dob': formated_dob,
                                            'line1': line1, 'line2': line2, 'line3':line3, 'line4':line4, 'line5':line5, 'line6':line6,
                                            'number_code': number_code, 'range1':splitted_number_code[0], 'range2': splitted_number_code[1],
                                            'range3': splitted_number_code[2], 'family_code_meaning': personal_chart['family_code_meaning'],
                                            'foundation_code_meaning': personal_chart['foundation_code_meaning'], 'social_code_meaning': personal_chart['social_code_meaning'],
                                            'other_codes': other_codes, 'status': True, 'cart_count': cart_count,
                    })