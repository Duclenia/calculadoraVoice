import speech_recognition as sr
import pyttsx3
import math
import re

engine = pyttsx3.init()
engine.setProperty('volume', 0.9)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def configurar_voz():
    vozes = engine.getProperty('voices')
    for voz in vozes:
        if 'brazil' in voz.id.lower() or 'portuguese' in voz.id.lower():
            engine.setProperty('voice', voz.id)
            break

def ouvir_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga o cálculo que você deseja fazer...")
        recognizer.adjust_for_ambient_noise(source)
        recognizer.dynamic_energy_threshold = True
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

    try:
        comando = recognizer.recognize_google(audio, language="pt-BR")
        print(f"Você disse: {comando}")
        return comando
    except sr.UnknownValueError:
        print("Não consegui entender. Tente novamente.")
        return None
    except sr.RequestError:
        print("Erro de conexão com o serviço de reconhecimento de fala.")
        return None

def calcular_e_falar(expressao):
    try:
        # Substitui palavras por operadores matemáticos
        expressao = expressao.lower()
        expressao = expressao.replace("multiplicado por", "*")
        expressao = expressao.replace("dividido por", "/")
        expressao = expressao.replace("mais", "+")
        expressao = expressao.replace("menos", "-")

        if 'raiz' in expressao:
            num = float(expressao.split('de')[-1].strip())  # Extrai número após 'de'
            resultado = math.sqrt(num)

        elif 'elevado' in expressao or 'potência' in expressao:
            partes = expressao.split()
            base = float(partes[0])
            expoente = float(partes[-1])
            resultado = base ** expoente
            
        elif 'sen' in expressao:
            num = float(expressao.split(' ')[-1].strip())
            resultado = math.sin(math.radians(num))

        elif 'cos' in expressao:
            num = float(expressao.split(' ')[-1].strip())
            resultado = math.cos(math.radians(num))

        elif 'multiplicado por' in expressao:
            partes = expressao.split()
            num1 = float(partes[0].strip())
            num2 = float(partes[2].strip())
            resultado = num1 * num2

        else:
            resultado = eval(expressao)

        print(f"O resultado é: {resultado}")
        engine.say(f"O resultado é {resultado}")
        engine.runAndWait()

    except Exception as e:
        print(f"Erro ao calcular: {e}")
        engine.say("Desculpe, houve um erro ao calcular.")
        engine.runAndWait()

def calculadora_por_fala():
    configurar_voz()
    speak("Olá! Eu sou a calculadora de voz. Como posso ajudar?")
    while True:
        comando = ouvir_comando()
        if comando:
            if "parar" in comando.lower() or 'sair' in comando.lower():
                print("Finalizando a calculadora...")
                engine.say("Finalizando a calculadora...")
                engine.runAndWait()
                break
            else:
                calcular_e_falar(comando)

calculadora_por_fala()
