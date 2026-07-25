
# My Dictionary

من تواجهك كلمات جديدة بلغة ثانية تبي تتعلمها تحتار وين تكتبها وغالبا اذا بيكون يدوي ماراح يكون عملي.
**عشان كذا جيت بهالحل** الا وهو انك تخزن 
1. .الكلمة
2. الشرح لها باللغة نفسها.
3. الكلمة بلغتك الام. 

بطريقة سريعة وبسيطة

--- 

## اللغات المستخدمة لبناء هالمشروع
* Python
* SQLite

**ليش استخدمت SQLite؟** لان المشروع متوقع يكون حجم الداتا صغير ويستهدف فقط الشخص المالك للجهاز ومو عدة اشخاص ف مافي غرض لاستخدام داتا بيسز اعقد.

## الفكرة الحالية للبرنامج

اول ماتشغل السكربت راح يسألك
1. تبي تضيف كلمة؟
2. تبي تشوف الكلمات المضافة؟
3. تبي تبحث عن كلمة معينة يطلع لك جميع نتايجها؟ 

### قسم اضافة الكلمة

لم تختار خيار اضافة الكلمة راح يسالك البرنامج عن الكلمة والشرح لها ومعناها بلغتك الام.

بالنسبة للتيبل راح يسوي جدولين الا وهو 
* words
* definition

عند words راح تكون الاعمدة هم 
word_id, name, insert_date

```sqlite
CREATE TABLE IF NOT EXISTS words (
                word_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                insert_date DATE DEFAULT CURRENT_TIMESTAMP
            );
```

وعند الdefinition الاعمدة بتكون  
id, defi, native_word, insert_date, word_id

```sqlite
CREATE TABLE IF NOT EXISTS definition (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                defi TEXT NOT NULL,
                native_word TEXT,
                insert_date DATE DEFAULT CURRENT_TIMESTAMP,
                word_id INTEGER,
                FOREIGN KEY (word_id) REFERENCES words(id)
            );
```

### قسم عرض النتيجة 

راح يعرض لك الاعمدة هذي من اليسار لليمين: 

ID    | NAME            | DEFINITION                          | FREQ    | INSERT DATE          | NATIVE WORD 

طبعا خليت السكربت يكون مهتم جدا بالمساحات بحيث يكون الشكل واضح ومريح للعين

و حاليا الصفوف تمشي بترتيب ال ID لكن مستقبل راح اخلي المستخدم هو اللي يقرر يمشي على ايش