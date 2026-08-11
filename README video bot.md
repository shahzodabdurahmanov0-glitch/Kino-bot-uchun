# Raqam bo'yicha Video Yetkazish Boti

Foydalanuvchi botga raqam yuboradi (masalan `1`, `2`, `15`) — bot Telegram kanalidagi mos
videoni topib, foydalanuvchiga jo'natadi. Videolar kanalda saqlanadi, bot ularni faqat
ko'chirib (copy) yuboradi.

## Tuzilma: 2 ta kanal + 1 bot

- **Ombor kanal** (yopiq, faqat siz uchun) — barcha videolar shu yerda saqlanadi. Botning
  `CHANNEL_ID` sozlamasi shu kanalga ishora qiladi. Bu kanal odamlarga ko'rinmaydi.
- **Tizer kanal** (ochiq, hammaga ko'rinadi) — bu yerga siz qo'lda kino parchalarini
  joylaysiz, tagiga "kodni bilmasangiz botga o'ting: @sizning_botingiz" deb yozasiz. Bu
  kanalga botning texnik aloqasi shart emas, siz uni oddiy Telegram kanal sifatida
  boshqarasiz. Bot esa, aksincha, kodi bilmagan yoki noto'g'ri yozgan odamlarni shu
  kanalga (`TEASER_CHANNEL_LINK` orqali) avtomatik yo'naltiradi.

## 1. Kanal va bot sozlash

1. Telegram'da yangi **kanal** yarating (public yoki private — farqi yo'q) va videolaringizni
   shu yerga joylang.
2. [@BotFather](https://t.me/BotFather) orqali bot yarating, tokenni oling.
3. Botni kanalga **administrator** sifatida qo'shing (kamida "Post Messages" huquqisiz ham
   ishlaydi, lekin admin bo'lishi shart — aks holda bot kanal ichidagi xabarlarni o'qiy olmaydi).
4. Kanal ID'sini oling — eng oson yo'li: kanalga biror xabar yuborib, uni
   [@userinfobot](https://t.me/userinfobot) yoki [@getidsbot](https://t.me/getidsbot)ga forward
   qiling, u sizga kanalning raqamli ID'sini beradi (odatda `-100` bilan boshlanadi).
5. O'zingizning shaxsiy Telegram ID'ingizni ham xuddi shu bot orqali oling — bu `ADMIN_ID`
   bo'ladi (faqat siz raqamlarni videolarga bog'lay olasiz).

## 2. O'rnatish

```bash
pip install -r requirements.txt
export TELEGRAM_BOT_TOKEN="sizning_tokeningiz"
export CHANNEL_ID="-100xxxxxxxxxx"
export ADMIN_ID="sizning_user_id_ingiz"
export TEASER_CHANNEL_LINK="https://t.me/tizer_kanalingiz"
python video_delivery_bot.py
```

Doim ishlab turishi uchun botni Railway, Render yoki VPS'ga joylashtiring.

## 3. Videolarga raqam bog'lash

1. Admin sifatida kanaldagi videoni **botga forward qiling** (kanaldan to'g'ridan-to'g'ri
   forward, boshqa joydan emas).
2. Bot sizdan shu videoga qaysi raqamni berishni so'raydi.
3. Raqamni oddiy xabar sifatida yozing (masalan `7`) — bot uni saqlab qo'yadi.
4. Barcha bog'langan raqamlarni ko'rish uchun botga `/list` yuboring (faqat admin uchun
   ishlaydi).

## 4. Foydalanuvchi tomonidan ishlatilishi

Har qanday foydalanuvchi botga raqam yuborsa (masalan `7`), bot mos videoni kanaldan olib,
to'g'ridan-to'g'ri o'sha foydalanuvchiga jo'natadi.

## 5. Kompyuter yoqiq turmasa ham 24/7 ishlashi uchun (Render.com, tekin)

Bot kodi shunday yozilganki, Render'ga joylasangiz avtomatik "webhook" rejimiga o'tadi —
alohida sozlash shart emas.

1. Shu fayllarni (`video_delivery_bot.py`, `requirements.txt`) GitHub'da yangi repository
   (masalan `kino-bot`) ochib, shu yerga yuklang.
2. [render.com](https://render.com)da bepul ro'yxatdan o'ting (kredit karta so'ramaydi),
   GitHub akkauntingizni ulang.
3. Dashboard'da **New → Web Service** tanlang, yaratgan repositoryingizni tanlang.
4. Sozlamalarda:
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python video_delivery_bot.py`
5. **Environment** bo'limida quyidagi o'zgaruvchilarni qo'shing: `TELEGRAM_BOT_TOKEN`,
   `CHANNEL_ID`, `ADMIN_ID` (3-punktdagi kabi) va `TEASER_CHANNEL_LINK` (tizer kanalingiz
   havolasi, masalan `https://t.me/tizer_kanalingiz`).
6. **Create Web Service** tugmasini bosing — bir necha daqiqada bot ishga tushadi va
   kompyuteringiz o'chiq bo'lsa ham 24/7 ishlab turadi.
7. (Tavsiya) Render'ning bepul tarifi 15 daqiqa xabar kelmasa "uxlab qoladi", birinchi
   xabarga sekinroq javob berishi mumkin. Buni oldini olish uchun
   [UptimeRobot](https://uptimerobot.com)da bepul monitor yarating va Render bergan
   URL'ingizni (masalan `https://kino-bot.onrender.com`) har 10-14 daqiqada "ping"
   qilib turishini sozlang.

## Eslatmalar

- Bog'lanishlar `video_map.json` faylida saqlanadi. Serverni qayta ishga tushirsangiz ham bu
  fayl saqlanib qoladi (agar hosting'ingiz disk saqlashni qo'llab-quvvatlasa). Katta hajmda
  ishlatmoqchi bo'lsangiz, buni SQLite yoki boshqa bazaga ko'chirish tavsiya etiladi.
- `copy_message` funksiyasi videoni "forwarded from" belgisisiz, xuddi bot o'zi yuborayotgandek
  jo'natadi.
- Kanal **private** bo'lsa ham bot ishlayveradi, chunki bot admin sifatida a'zo — foydalanuvchi
  kanalga a'zo bo'lishi shart emas, faqat bot bilan gaplashadi.
