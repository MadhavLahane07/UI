from django.shortcuts import render
import os
from .predict import predict_audio 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect

translations = {
    "en": {
        "title": "TrueVoice AI",
        "detect": "Detect",
        "history": "History",
        "logout": "Logout"
    },
    "hi": {
        "title": "ट्रूवॉइस एआई",
        "detect": "जांच करें",
        "history": "इतिहास",
        "logout": "लॉगआउट"
    },
    "mr": {
        "title": "ट्रूवॉइस एआई",
        "detect": "तपासा",
        "history": "इतिहास",
        "logout": "बाहेर पडा"
    }
}

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')

    lang = request.GET.get('lang', 'en')  # default English
    text = translations.get(lang, translations['en'])

    return render(request, "index.html", {
        "text": text,
        "lang": lang
    })

from .models import Prediction

def predict(request):
    if request.method == "POST":
        audio_file = request.FILES['audio']

        # 🌍 GET LANGUAGE
        lang = request.POST.get('lang', 'en')
        text = translations.get(lang, translations['en'])

        file_path = "temp.wav"

        with open(file_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        result, confidence = predict_audio(file_path)

        # SAVE HISTORY
        Prediction.objects.create(
            user=request.user,
            result=result,
            confidence=confidence * 100
        )

        os.remove(file_path)

        return render(request, "result.html", {
            "result": result,
            "confidence": round(confidence * 100, 2),
            "text": text,
            "lang": lang
        })

    return redirect('home')


def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(username=username, password=password)
        user.save()

        return redirect('login')

    return render(request, "signup.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('login')

def history(request):
    data = Prediction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "history.html", {"data": data})
