"""
═══════════════════════════════════════════════════════════════════════════════
    بلاجن KANZ88 الاحترافي لـ phBot
    Professional Plugin for Silkroad Online Bot
    
    المطور: KANZ88
    الإصدار: 1.0.0
    التاريخ: 2026
═══════════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════════
# 📦 IMPORTS - المكتبات المستخدمة
# ═══════════════════════════════════════════════════════════════════════════════
import phBot
from phBot import *
import QtBind
import json
import os
import time

# ═══════════════════════════════════════════════════════════════════════════════
# 🔧 PLUGIN INFO - معلومات البلاجن (إلزامية)
# ═══════════════════════════════════════════════════════════════════════════════
pName = "KANZ88_Plugin"                                    # اسم البلاجن
pVersion = "1.0.0"                                         # رقم الإصدار
pGuid = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"           # المعرف الفريد

# ═══════════════════════════════════════════════════════════════════════════════
# ⚙️ SETTINGS SECTION - قسم الإعدادات
# ═══════════════════════════════════════════════════════════════════════════════

# --- إعدادات المراقبة والتحذيرات ---
HP_WARNING_THRESHOLD = 50                                  # نسبة تحذير HP (بالنسبة المئوية)
POSITION_PRINT_INTERVAL = 1.0                             # وقت طباعة الإحداثيات (بالثواني)

# --- إعدادات الرد التلقائي ---
AUTO_REPLY_ENABLED = True                                 # تفعيل الرد التلقائي
AUTO_REPLY_MESSAGE = "Hello"                              # رسالة الرد التلقائي

# --- إعدادات الواجهة ---
GUI_WIDTH = 400                                           # عرض نافذة البلاجن
GUI_HEIGHT = 500                                          # ارتفاع نافذة البلاجن

# ═══════════════════════════════════════════════════════════════════════════════
# 📊 GLOBAL STATE - المتغيرات العامة لتتبع الحالة
# ═══════════════════════════════════════════════════════════════════════════════
last_position_print = 0                                    # آخر وقت طباعة الإحداثيات
last_hp_warning = False                                    # حالة تحذير HP السابقة
gui = None                                                 # كائن الواجهة الرسومية
inGame = False                                             # حالة تواجد الشخصية في اللعبة

# ═══════════════════════════════════════════════════════════════════════════════
# 🖥️ GUI SECTION - قسم الواجهة الرسومية
# ═══════════════════════════════════════════════════════════════════════════════

def create_gui():
    """إنشاء الواجهة الرسومية للبلاجن"""
    global gui
    
    gui = {}
    
    # --- النافذة الرئيسية ---
    gui['window'] = QtBind.createDialog("KANZ88 Plugin Settings", GUI_WIDTH, GUI_HEIGHT)
    QtBind.setWindowTitle(gui['window'], f"{pName} v{pVersion}")
    
    # --- قسم المعلومات ---
    y_pos = 10
    QtBind.createLabel(gui['window'], "═══════════ معلومات البلاجن ═══════════", 10, y_pos, 380, 20)
    y_pos += 25
    gui['lblInfo'] = QtBind.createLabel(gui['window'], "الحالة: في انتظار الاتصال...", 10, y_pos, 380, 20)
    y_pos += 25
    gui['lblCharName'] = QtBind.createLabel(gui['window'], "الشخصية: غير متصل", 10, y_pos, 380, 20)
    y_pos += 30
    
    # --- قسم مراقبة HP ---
    QtBind.createLabel(gui['window'], "═══════════ مراقبة HP ═══════════", 10, y_pos, 380, 20)
    y_pos += 25
    gui['cbHPMonitor'] = QtBind.createCheckBox(gui['window'], 'تفعيل مراقبة HP', 20, y_pos, lambda: save_settings())
    QtBind.setChecked(gui['cbHPMonitor'], True)
    y_pos += 25
    QtBind.createLabel(gui['window'], "نسبة التحذير (%):", 20, y_pos, 150, 20)
    gui['txtHPThreshold'] = QtBind.createLineEdit(gui['window'], str(HP_WARNING_THRESHOLD), 180, y_pos, 100, 20)
    y_pos += 25
    gui['lblHPStatus'] = QtBind.createLabel(gui['window'], "حالة HP: جاري المراقبة...", 20, y_pos, 360, 20)
    y_pos += 30
    
    # --- قسم طباعة الإحداثيات ---
    QtBind.createLabel(gui['window'], "═══════════ الإحداثيات ═══════════", 10, y_pos, 380, 20)
    y_pos += 25
    gui['cbPositionPrint'] = QtBind.createCheckBox(gui['window'], 'تفعيل طباعة الإحداثيات', 20, y_pos, lambda: save_settings())
    QtBind.setChecked(gui['cbPositionPrint'], True)
    y_pos += 25
    gui['lblPosition'] = QtBind.createLabel(gui['window'], "الموقع: X: 0.0, Y: 0.0, Z: 0.0", 20, y_pos, 360, 20)
    y_pos += 30
    
    # --- قسم الرد التلقائي ---
    QtBind.createLabel(gui['window'], "═══════════ الرد التلقائي ═══════════", 10, y_pos, 380, 20)
    y_pos += 25
    gui['cbAutoReply'] = QtBind.createCheckBox(gui['window'], 'تفعيل الرد التلقائي', 20, y_pos, lambda: save_settings())
    QtBind.setChecked(gui['cbAutoReply'], AUTO_REPLY_ENABLED)
    y_pos += 25
    QtBind.createLabel(gui['window'], "رسالة الرد:", 20, y_pos, 100, 20)
    gui['txtReplyMsg'] = QtBind.createLineEdit(gui['window'], AUTO_REPLY_MESSAGE, 130, y_pos, 250, 20)
    y_pos += 25
    gui['lblReplyStatus'] = QtBind.createLabel(gui['window'], "آخر رد: لا يوجد", 20, y_pos, 360, 20)
    y_pos += 30
    
    # --- قسم الإحصائيات ---
    QtBind.createLabel(gui['window'], "═══════════ الإحصائيات ═══════════", 10, y_pos, 380, 20)
    y_pos += 25
    gui['lblStats'] = QtBind.createLabel(gui['window'], "إجمالي الردود: 0 | التحذيرات: 0", 20, y_pos, 360, 20)
    y_pos += 30
    
    # --- أزرار التحكم ---
    gui['btnSave'] = QtBind.createButton(gui['window'], 'حفظ الإعدادات', 20, y_pos, 170, 25, save_settings)
    gui['btnReset'] = QtBind.createButton(gui['window'], 'إعادة تعيين', 210, y_pos, 170, 25, reset_settings)
    
    # تحميل الإعدادات المحفوظة
    load_settings()
    
    log(f"✅ تم إنشاء واجهة {pName} بنجاح")

def save_settings():
    """حفظ إعدادات البلاجن"""
    if gui:
        settings = {
            'hp_monitor': QtBind.isChecked(gui['cbHPMonitor']),
            'hp_threshold': QtBind.text(gui['txtHPThreshold']),
            'position_print': QtBind.isChecked(gui['cbPositionPrint']),
            'auto_reply': QtBind.isChecked(gui['cbAutoReply']),
            'reply_message': QtBind.text(gui['txtReplyMsg'])
        }
        
        # حفظ في ملف JSON
        config_path = get_config_path()
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, ensure_ascii=False, indent=4)
        
        log("💾 تم حفظ الإعدادات بنجاح")

def load_settings():
    """تحميل إعدادات البلاجن"""
    global HP_WARNING_THRESHOLD, AUTO_REPLY_ENABLED, AUTO_REPLY_MESSAGE
    
    config_path = get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            if gui:
                QtBind.setChecked(gui['cbHPMonitor'], settings.get('hp_monitor', True))
                QtBind.setText(gui['txtHPThreshold'], settings.get('hp_threshold', '50'))
                QtBind.setChecked(gui['cbPositionPrint'], settings.get('position_print', True))
                QtBind.setChecked(gui['cbAutoReply'], settings.get('auto_reply', True))
                QtBind.setText(gui['txtReplyMsg'], settings.get('reply_message', 'Hello'))
            
            HP_WARNING_THRESHOLD = int(settings.get('hp_threshold', 50))
            AUTO_REPLY_ENABLED = settings.get('auto_reply', True)
            AUTO_REPLY_MESSAGE = settings.get('reply_message', 'Hello')
            
            log("📂 تم تحميل الإعدادات المحفوظة")
        except Exception as e:
            log(f"⚠️ خطأ في تحميل الإعدادات: {str(e)}")

def reset_settings():
    """إعادة تعيين الإعدادات إلى القيم الافتراضية"""
    if gui:
        QtBind.setChecked(gui['cbHPMonitor'], True)
        QtBind.setText(gui['txtHPThreshold'], '50')
        QtBind.setChecked(gui['cbPositionPrint'], True)
        QtBind.setChecked(gui['cbAutoReply'], True)
        QtBind.setText(gui['txtReplyMsg'], 'Hello')
        save_settings()
        log("🔄 تم إعادة تعيين الإعدادات")

def get_config_path():
    """الحصول على مسار ملف الإعدادات"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{pName}_config.json")

def update_gui_info():
    """تحديث معلومات الواجهة"""
    if gui and inGame:
        character = get_character_data()
        if character:
            # تحديث اسم الشخصية
            char_name = character.get('name', 'غير معروف')
            QtBind.setText(gui['lblCharName'], f"الشخصية: {char_name}")
            
            # تحديث حالة HP
            hp = character.get('hp', 0)
            max_hp = character.get('max_hp', 1)
            hp_percent = (hp / max_hp * 100) if max_hp > 0 else 0
            QtBind.setText(gui['lblHPStatus'], f"حالة HP: {hp}/{max_hp} ({hp_percent:.1f}%)")
            
            # تحديث الموقع
            position = get_position()
            if position:
                x, y, z = position['x'], position['y'], position['z']
                QtBind.setText(gui['lblPosition'], f"الموقع: X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")

# ═══════════════════════════════════════════════════════════════════════════════
# 🛠️ FUNCTIONS SECTION - قسم الوظائف
# ═══════════════════════════════════════════════════════════════════════════════

# --- وظائف المساعدة ---

def get_character_data():
    """
    الحصول على بيانات الشخصية
    Returns: قاموس يحتوي على معلومات الشخصية أو None
    """
    try:
        character = get_character()
        return character
    except Exception:
        return None

def get_position():
    """
    الحصول على موقع الشخصية الحالي
    Returns: قاموس يحتوي على الإحداثيات (x, y, z) أو None
    """
    try:
        character = get_character()
        if character:
            return {
                'x': character.get('x', 0),
                'y': character.get('y', 0),
                'z': character.get('z', 0),
                'region': character.get('region', 0)
            }
    except Exception:
        pass
    return None

# --- وظيفة مراقبة HP ---

def monitor_hp():
    """مراقبة دم الشخصية وإصدار تحذير عند انخفاضه"""
    global last_hp_warning
    
    # التحقق من تفعيل المراقبة من الواجهة
    if gui and not QtBind.isChecked(gui['cbHPMonitor']):
        return
    
    character = get_character_data()
    if not character:
        return
    
    current_hp = character.get('hp', 0)
    max_hp = character.get('max_hp', 1)
    
    if max_hp > 0:
        hp_percent = (current_hp / max_hp) * 100
        
        # الحصول على قيمة التحذير من الواجهة
        threshold = HP_WARNING_THRESHOLD
        if gui:
            try:
                threshold = int(QtBind.text(gui['txtHPThreshold']))
            except:
                threshold = 50
        
        if hp_percent < threshold:
            if not last_hp_warning:
                log(f"⚠️ تحذير! دم الشخصية منخفض: {hp_percent:.1f}% ({current_hp}/{max_hp})")
                last_hp_warning = True
        else:
            last_hp_warning = False

# --- وظيفة طباعة الإحداثيات ---

def print_position():
    """طباعة إحداثيات الموقع الحالي"""
    global last_position_print
    
    # التحقق من تفعيل الطباعة من الواجهة
    if gui and not QtBind.isChecked(gui['cbPositionPrint']):
        return
    
    current_time = time.time()
    
    if current_time - last_position_print >= POSITION_PRINT_INTERVAL:
        position = get_position()
        
        if position:
            x, y, z = position['x'], position['y'], position['z']
            region = position.get('region', 'غير معروف')
            log(f"📍 الموقع الحالي - X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f} | المنطقة: {region}")
        
        last_position_print = current_time

# --- وظيفة الرد التلقائي ---

def handle_private_message(player_name, message):
    """
    معالجة الرسائل الخاصة والرد التلقائي
    Args:
        player_name: اسم اللاعب المرسل
        message: نص الرسالة
    """
    # التحقق من تفعيل الرد التلقائي
    enabled = AUTO_REPLY_ENABLED
    reply_msg = AUTO_REPLY_MESSAGE
    
    if gui:
        enabled = QtBind.isChecked(gui['cbAutoReply'])
        reply_msg = QtBind.text(gui['txtReplyMsg'])
    
    if not enabled:
        return
    
    log(f"📨 استقبلت رسالة خاصة من {player_name}: {message}")
    
    # إرسال الرد التلقائي
    phBot.chat(f"/pm {player_name} {reply_msg}")
    
    log(f"✉️ تم إرسال رد تلقائي '{reply_msg}' إلى {player_name}")
    
    # تحديث الواجهة
    if gui:
        QtBind.setText(gui['lblReplyStatus'], f"آخر رد: {player_name}")

# ═══════════════════════════════════════════════════════════════════════════════
# 🎯 EVENTS SECTION - قسم الأحداث
# ═══════════════════════════════════════════════════════════════════════════════

def event_loop():
    """
    الحلقة الرئيسية - تُستدعى بشكل متكرر كل ~500 مللي ثانية
    تقوم بتنفيذ جميع الوظائف الدورية
    """
    global inGame
    
    if not inGame:
        return
    
    # تنفيذ وظائف المراقبة
    monitor_hp()           # مراقبة دم الشخصية
    print_position()       # طباعة الإحداثيات
    
    # تحديث الواجهة
    if gui:
        update_gui_info()


def handle_event(event_type, data):
    """
    معالج الأحداث الرئيسي - يتعامل مع أحداث اللعبة المختلفة
    Args:
        event_type: نوع الحدث (0-5)
        data: بيانات الحدث
    """
    global inGame
    
    if event_type == 0:                                    # البوت بدأ
        log("✅ البوت بدأ التشغيل")
        if gui:
            QtBind.setText(gui['lblInfo'], "الحالة: البوت قيد التشغيل")
    
    elif event_type == 1:                                  # البوت توقف
        log("🛑 البوت توقف عن التشغيل")
        inGame = False
        if gui:
            QtBind.setText(gui['lblInfo'], "الحالة: البوت متوقف")
    
    elif event_type == 2:                                  # اتصل بالسيرفر
        log("🌐 تم الاتصال بالسيرفر بنجاح")
        if gui:
            QtBind.setText(gui['lblInfo'], "الحالة: متصل بالسيرفر")
    
    elif event_type == 3:                                  # انقطع الاتصال
        log("❌ انقطع الاتصال بالسيرفر")
        inGame = False
        if gui:
            QtBind.setText(gui['lblInfo'], "الحالة: غير متصل")
    
    elif event_type == 4:                                  # دخول اللعبة
        log("🎮 الشخصية دخلت عالم اللعبة")
        inGame = True
        if gui:
            QtBind.setText(gui['lblInfo'], "الحالة: في اللعبة")
    
    elif event_type == 5:                                  # موت الشخصية
        log("💀 الشخصية ماتت! جاري إعادة الإحياء...")
        if gui:
            QtBind.setText(gui['lblInfo'], "الحالة: الشخصية ميتة")

def joined_game():
    """حدث دخول الشخصية إلى اللعبة - رسالة الترحيب"""
    global inGame
    inGame = True
    
    # رسالة ترحيب KANZ88
    log("=" * 60)
    log("🎉 مرحباً KANZ88! 🎉")
    log("تم تحميل البلاجن بنجاح")
    log("=" * 60)
    
    # عرض معلومات الشخصية
    character = get_character_data()
    if character:
        char_name = character.get('name', 'غير معروف')
        char_level = character.get('level', 0)
        char_hp = character.get('hp', 0)
        char_max_hp = character.get('max_hp', 0)
        char_mp = character.get('mp', 0)
        char_max_mp = character.get('max_mp', 0)
        
        log(f"📊 معلومات الشخصية:")
        log(f"   الاسم: {char_name}")
        log(f"   المستوى: {char_level}")
        log(f"   HP: {char_hp}/{char_max_hp}")
        log(f"   MP: {char_mp}/{char_max_mp}")
    
    log("=" * 60)
    
    # تحديث الواجهة
    if gui:
        QtBind.setText(gui['lblInfo'], "الحالة: في اللعبة")
        if character:
            QtBind.setText(gui['lblCharName'], f"الشخصية: {character.get('name', 'غير معروف')}")

def handle_chat(message_type, player_name, message):
    """
    معالج رسائل الشات
    Args:
        message_type: نوع الرسالة (1=عامة, 2=خاصة, 3=حزب, إلخ)
        player_name: اسم اللاعب
        message: نص الرسالة
    """
    if message_type == 2:                                  # رسالة خاصة
        handle_private_message(player_name, message)

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 INITIALIZATION - التهيئة والبداية
# ═══════════════════════════════════════════════════════════════════════════════

# إنشاء الواجهة الرسومية
create_gui()

# طباعة رسالة التحميل
log("=" * 60)
log(f"🔌 تم تحميل بلاجن {pName} - الإصدار {pVersion}")
log("👤 مُصمم خصيصاً لـ KANZ88")
log("=" * 60)
log("✨ الميزات المفعّلة:")
log("   ✓ واجهة رسومية احترافية في تبويب Plugins")
log("   ✓ رسالة ترحيب عند دخول اللعبة")
log("   ✓ مراقبة دم الشخصية (تحذير عند الانخفاض)")
log("   ✓ طباعة الإحداثيات بشكل دوري")
log(f"   ✓ رد تلقائي '{AUTO_REPLY_MESSAGE}' على الرسائل الخاصة")
log("=" * 60)

# التحقق من GUID
if pGuid == "00000000-0000-0000-0000-000000000000":
    log("⚠️ تحذير: يُرجى تغيير GUID إلى معرف فريد!")

log(f"✅ {pName} جاهز للعمل!")
log("=" * 60)
