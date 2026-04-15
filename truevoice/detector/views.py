from django.shortcuts import render, redirect
import os
from .predict import predict_audio
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Prediction

translations = {
    "en": {
        "title": "TrueVoice AI",
        "detect": "Detect",
        "history": "History",
        "logout": "Logout",
        "result": "Analysis Result",
        "confidence": "Confidence",
        "real": "Real Voice",
        "fake": "Deepfake Voice",
        "back": "Back"
    },
    "hi": {
        "title": "ट्रूवॉइस एआई",
        "detect": "जांच करें",
        "history": "इतिहास",
        "logout": "लॉगआउट",
        "result": "विश्लेषण परिणाम",
        "confidence": "विश्वास स्तर",
        "real": "वास्तविक आवाज",
        "fake": "नकली आवाज",
        "back": "वापस जाएं"
    },
    "mr": {
        "title": "ट्रूवॉइस एआई",
        "detect": "तपासा",
        "history": "इतिहास",
        "logout": "बाहेर पडा",
        "result": "विश्लेषण निकाल",
        "confidence": "विश्वास पातळी",
        "real": "खरी आवाज",
        "fake": "बनावट आवाज",
        "back": "मागे जा"
    }
}

# ✅ HOME PAGE PUBLIC
def home(request):
    lang = request.GET.get('lang', 'en')
    text = translations.get(lang, translations['en'])

    return render(request, "index.html", {
        "text": text,
        "lang": lang
    })


# ✅ LOGIN REQUIRED FOR PREDICT
@login_required(login_url='login')
def predict(request):
    if request.method == "POST":
        audio_file = request.FILES['audio']

        lang = request.POST.get('lang', 'en')
        text = translations.get(lang, translations['en'])

        file_path = "temp.wav"

        with open(file_path, 'wb+') as destination:
            for chunk in audio_file.chunks():
                destination.write(chunk)

        result, confidence = predict_audio(file_path)

        if "Real" in result:
            result_type = "real"
            result_text = text["real"]
        else:
            result_type = "fake"
            result_text = text["fake"]

        Prediction.objects.create(
            user=request.user,
            result=result,
            confidence=confidence * 100,
            audio_file=audio_file.name
        )

        os.remove(file_path)

        return render(request, "result.html", {
            "result": result_text,
            "result_type": result_type,
            "confidence": round(confidence * 100, 2),
            "text": text,
            "lang": lang
        })

    return redirect('home')


# ✅ SIGNUP
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('signup')

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, "signup.html")


# ✅ LOGIN
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# ✅ LOGOUT → HOME PAGE
def logout_view(request):
    logout(request)
    return redirect('home')


# ✅ HISTORY LOGIN REQUIRED
@login_required(login_url='login')
def history(request):
    data = Prediction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "history.html", {"data": data})


# ✅ LANGUAGE PAGES LOGIN REQUIRED
@login_required(login_url='login')
def english(request):
    return render(request, 'english.html')


@login_required(login_url='login')
def marathi(request):
    return render(request, 'marathi.html')


@login_required(login_url='login')
def hindi(request):
    return render(request, 'hindi.html')