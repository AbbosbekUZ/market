from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from .models import Bolim, Mahsulot, Sotuv, Xarajat

from django.shortcuts import render
from django.db.models import Sum
from .models import Kirim, Sotuv, Xarajat

def home_view(request):
    bolimlar = Bolim.objects.all()
    mahsulotlar = Mahsulot.objects.all()
    sotuvlar = Sotuv.objects.all()
    xarajatlar = Xarajat.objects.all()
    kirimlar = Kirim.objects.all()  # Kirimlarni olish

    # Umumiy foyda, xarajat va sof foydani hisoblash
    jami_foyda = Sotuv.objects.aggregate(Sum('jami_summa'))['jami_summa__sum'] or 0
    jami_xarajat = Xarajat.objects.aggregate(Sum('miqdor'))['miqdor__sum'] or 0
    sof_foyda = jami_foyda - jami_xarajat

    # Eng ko'p sotilgan 3 mahsulot
    top_mahsulotlar = Sotuv.objects.values('mahsulot__nom').annotate(
        jami_sotilgan=Sum('miqdor')
    ).order_by('-jami_sotilgan')[:3]

    return render(request, 'home.html', {
        'bolimlar': bolimlar,
        'mahsulotlar': mahsulotlar,
        'sotuvlar': sotuvlar,
        'xarajatlar': xarajatlar,
        'kirimlar': kirimlar,  # Kirimlar ma'lumotlarini uzatish
        'jami_foyda': jami_foyda,
        'jami_xarajat': jami_xarajat,
        'sof_foyda': sof_foyda,
        'top_mahsulotlar': top_mahsulotlar
    })
def bolim_view(request, bolim_id):
    bolim = get_object_or_404(Bolim, id=bolim_id)
    mahsulotlar = bolim.mahsulotlar.all()
    return render(request, 'bolim.html', {
        'bolim': bolim,
        'mahsulotlar': mahsulotlar
    })

def mahsulot_sotish(request, mahsulot_id):
    mahsulot = get_object_or_404(Mahsulot, id=mahsulot_id)

    if request.method == 'POST':
        try:
            miqdor = int(request.POST.get('miqdor', 0))

            if miqdor <= 0:
                messages.error(request, "Miqdor noto'g'ri")
            elif miqdor > mahsulot.miqdor:
                messages.error(request, "Yetarli mahsulot yo'q")
            else:
                jami_summa = mahsulot.narx2 * miqdor

                Sotuv.objects.create(
                    mahsulot=mahsulot,
                    miqdor=miqdor,
                    jami_summa=jami_summa,
                    izoh=request.POST.get('izoh', '')
                )

                mahsulot.miqdor -= miqdor  # Ombordagi mahsulot miqdorini kamaytirish
                mahsulot.save()

                messages.success(request, "Sotuv muvaffaqiyatli amalga oshirildi")
                return redirect('home')

        except ValueError:
            messages.error(request, "Noto'g'ri miqdor kiritildi")

    return render(request, 'mahsulot_sotish.html', {'mahsulot': mahsulot})

def statistika_view(request):
    oxirgi_30_kun = timezone.now().date() - timedelta(days=30)

    jami_foyda = Sotuv.objects.aggregate(Sum('jami_summa'))['jami_summa__sum'] or 0
    jami_xarajat = Xarajat.objects.aggregate(Sum('miqdor'))['miqdor__sum'] or 0
    sof_foyda = jami_foyda - jami_xarajat

    oxirgi_30_kun_sotuvlari = Sotuv.objects.filter(sana__gte=oxirgi_30_kun)
    top_mahsulotlar = Sotuv.objects.values('mahsulot__nom').annotate(
        jami_sotilgan=Sum('miqdor')
    ).order_by('-jami_sotilgan')[:3]

    return render(request, 'statistika.html', {
        'jami_foyda': jami_foyda,
        'jami_xarajat': jami_xarajat,
        'sof_foyda': sof_foyda,
        'oxirgi_30_kun_sotuvlari': oxirgi_30_kun_sotuvlari,
        'top_mahsulotlar': top_mahsulotlar
    })
