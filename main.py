import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from database import Database
from datetime import datetime
import json

class AccountingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("برنامج المحاسبة المبسط")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        # تعيين الاتجاه من اليمين إلى اليسار
        self.root.tk.call('tk', 'scaling', 2.0)
        
        self.db = Database()
        self.setup_ui()
    
    def setup_ui(self):
        """إعداد الواجهة الرسومية"""
        # شريط القوائم
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ملف", menu=file_menu)
        file_menu.add_command(label="خروج", command=self.root.quit)
        
        # النافذة الرئيسية
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # القائمة الجانبية
        sidebar_frame = ttk.Frame(main_frame)
        sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)
        
        ttk.Label(sidebar_frame, text="القوائم الرئيسية", font=("Arial", 12, "bold")).pack(pady=10)
        
        ttk.Button(sidebar_frame, text="➕ زبون جديد", 
                  command=self.show_add_customer).pack(fill=tk.X, pady=5)
        
        ttk.Button(sidebar_frame, text="📄 فاتورة جديدة", 
                  command=self.show_add_invoice).pack(fill=tk.X, pady=5)
        
        ttk.Button(sidebar_frame, text="💰 دفعة جديدة", 
                  command=self.show_add_payment).pack(fill=tk.X, pady=5)
        
        ttk.Button(sidebar_frame, text="📊 كشف الحساب", 
                  command=self.show_customer_statement).pack(fill=tk.X, pady=5)
        
        ttk.Button(sidebar_frame, text="🔍 عرض الفواتير", 
                  command=self.show_all_invoices).pack(fill=tk.X, pady=5)
        
        # المنطقة الرئيسية للمحتوى
        self.content_frame = ttk.Frame(main_frame)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # الترحيب
        welcome_label = ttk.Label(self.content_frame, 
                                  text="مرحباً بك في برنامج المحاسبة المبسط",
                                  font=("Arial", 14, "bold"))
        welcome_label.pack(pady=20)
        
        info_text = """
        هذا البرنامج يساعدك في تتبع:
        ✓ الزبائن والعملاء
        ✓ الفواتير والمبيعات
        ✓ الدفعات والتسديدات
        ✓ باقي الديون
        ✓ كشف حساب العملاء
        """
        
        ttk.Label(self.content_frame, text=info_text, 
                 font=("Arial", 11), justify=tk.LEFT).pack(pady=10)
    
    def clear_content(self):
        """مسح محتوى النافذة الرئيسية"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_add_customer(self):
        """نافذة إضافة زبون جديد"""
        self.clear_content()
        
        ttk.Label(self.content_frame, text="إضافة زبون جديد", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # اسم الزبون
        ttk.Label(self.content_frame, text="اسم الزبون:").pack(anchor=tk.E, padx=20)
        name_entry = ttk.Entry(self.content_frame, width=30)
        name_entry.pack(anchor=tk.E, padx=20, pady=5)
        
        # رقم الهاتف
        ttk.Label(self.content_frame, text="رقم الهاتف:").pack(anchor=tk.E, padx=20)
        phone_entry = ttk.Entry(self.content_frame, width=30)
        phone_entry.pack(anchor=tk.E, padx=20, pady=5)
        
        # العنوان
        ttk.Label(self.content_frame, text="العنوان:").pack(anchor=tk.E, padx=20)
        address_entry = ttk.Entry(self.content_frame, width=30)
        address_entry.pack(anchor=tk.E, padx=20, pady=5)
        
        def save_customer():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_entry.get().strip()
            
            if not name:
                messagebox.showerror("خطأ", "يجب إدخال اسم الزبون")
                return
            
            self.db.add_customer(name, phone, address)
            messagebox.showinfo("نجاح", f"تم إضافة الزبون: {name}")
            self.show_add_customer()
        
        ttk.Button(self.content_frame, text="💾 حفظ", 
                  command=save_customer).pack(pady=20)
    
    def show_add_invoice(self):
        """نافذة إضافة فاتورة جديدة"""
        self.clear_content()
        
        ttk.Label(self.content_frame, text="إضافة فاتورة جديدة", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # اختيار الزبون
        ttk.Label(self.content_frame, text="اختر الزبون:").pack(anchor=tk.E, padx=20)
        customers = self.db.get_all_customers()
        
        if not customers:
            messagebox.showwarning("تنبيه", "لا توجد زبائن. أضف زبون أولاً")
            return
        
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(self.content_frame, textvariable=customer_var, 
                                      width=30, state='readonly')
        customer_combo['values'] = [f"{c[1]} (ID: {c[0]})" for c in customers]
        customer_combo.pack(anchor=tk.E, padx=20, pady=5)
        
        # عدد الأمتار
        ttk.Label(self.content_frame, text="عدد الأمتار:").pack(anchor=tk.E, padx=20)
        meters_entry = ttk.Entry(self.content_frame, width=30)
        meters_entry.pack(anchor=tk.E, padx=20, pady=5)
        
        # سعر المتر
        ttk.Label(self.content_frame, text="سعر المتر:").pack(anchor=tk.E, padx=20)
        price_entry = ttk.Entry(self.content_frame, width=30)
        price_entry.pack(anchor=tk.E, padx=20, pady=5)
        
        # إجمالي المبلغ (محسوب تلقائياً)
        ttk.Label(self.content_frame, text="إجمالي المبلغ:").pack(anchor=tk.E, padx=20)
        total_label = ttk.Label(self.content_frame, text="0.00", font=("Arial", 12, "bold"))
        total_label.pack(anchor=tk.E, padx=20, pady=5)
        
        def calculate_total(*args):
            try:
                meters = float(meters_entry.get()) if meters_entry.get() else 0
                price = float(price_entry.get()) if price_entry.get() else 0
                total = meters * price
                total_label.config(text=f"{total:.2f}")
            except ValueError:
                total_label.config(text="0.00")
        
        meters_entry.bind('<KeyRelease>', calculate_total)
        price_entry.bind('<KeyRelease>', calculate_total)
        
        def save_invoice():
            if not customer_var.get():
                messagebox.showerror("خطأ", "اختر الزبون")
                return
            
            try:
                meters = float(meters_entry.get())
                price = float(price_entry.get())
                
                if meters <= 0 or price <= 0:
                    messagebox.showerror("خطأ", "يجب أن تكون القيم موجبة")
                    return
                
                customer_id = int(customer_var.get().split("ID: ")[1].rstrip(")"))
                self.db.add_invoice(customer_id, meters, price)
                messagebox.showinfo("نجاح", "تم إضافة الفاتورة بنجاح")
                self.show_add_invoice()
            except ValueError:
                messagebox.showerror("خطأ", "أدخل أرقام صحيحة")
        
        ttk.Button(self.content_frame, text="💾 حفظ الفاتورة", 
                  command=save_invoice).pack(pady=20)
    
    def show_add_payment(self):
        """نافذة إضافة دفعة"""
        self.clear_content()
        
        ttk.Label(self.content_frame, text="إضافة دفعة جديدة", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # اختيار الزبون
        ttk.Label(self.content_frame, text="اختر الزبون:").pack(anchor=tk.E, padx=20)
        customers = self.db.get_all_customers()
        
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(self.content_frame, textvariable=customer_var,
                                      width=30, state='readonly')
        customer_combo['values'] = [f"{c[1]} (ID: {c[0]})" for c in customers]
        customer_combo.pack(anchor=tk.E, padx=20, pady=5)
        
        # اختيار الفاتورة
        ttk.Label(self.content_frame, text="اختر الفاتورة:").pack(anchor=tk.E, padx=20)
        invoice_var = tk.StringVar()
        invoice_combo = ttk.Combobox(self.content_frame, textvariable=invoice_var,
                                     width=30, state='readonly')
        invoice_combo.pack(anchor=tk.E, padx=20, pady=5)
        
        def update_invoices(*args):
            try:
                customer_id = int(customer_var.get().split("ID: ")[1].rstrip(")"))
                conn = self.db.db_name
                import sqlite3
                conn = sqlite3.connect(self.db.db_name)
                c = conn.cursor()
                c.execute('''SELECT id, meters, total_amount, paid_amount, remaining_debt
                            FROM invoices WHERE customer_id = ? AND remaining_debt > 0''',
                         (customer_id,))
                invoices = c.fetchall()
                conn.close()
                
                invoice_combo['values'] = [
                    f"الفاتورة #{i[0]} - {i[1]} م - المتبقي: {i[4]:.2f}" for i in invoices
                ]
            except:
                invoice_combo['values'] = []
        
        customer_combo.bind('<<ComboboxSelected>>', update_invoices)
        
        # مبلغ الدفعة
        ttk.Label(self.content_frame, text="مبلغ الدفعة:").pack(anchor=tk.E, padx=20)
        amount_entry = ttk.Entry(self.content_frame, width=30)
        amount_entry.pack(anchor=tk.E, padx=20, pady=5)
        
        # ملاحظات
        ttk.Label(self.content_frame, text="ملاحظات (اختياري):").pack(anchor=tk.E, padx=20)
        notes_entry = ttk.Entry(self.content_frame, width=30)
        notes_entry.pack(anchor=tk.E, padx=20, pady=5)
        
        def save_payment():
            if not invoice_var.get():
                messagebox.showerror("خطأ", "اختر الفاتورة")
                return
            
            try:
                amount = float(amount_entry.get())
                if amount <= 0:
                    messagebox.showerror("خطأ", "يجب أن يكون المبلغ موجب")
                    return
                
                invoice_id = int(invoice_var.get().split("#")[1].split(" ")[0])
                notes = notes_entry.get().strip()
                
                self.db.add_payment(invoice_id, amount, notes)
                messagebox.showinfo("نجاح", "تم تسجيل الدفعة بنجاح")
                self.show_add_payment()
            except ValueError:
                messagebox.showerror("خطأ", "أدخل مبلغ صحيح")
        
        ttk.Button(self.content_frame, text="💾 حفظ الدفعة", 
                  command=save_payment).pack(pady=20)
    
    def show_customer_statement(self):
        """عرض كشف الحساب"""
        self.clear_content()
        
        ttk.Label(self.content_frame, text="كشف الحساب", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        # اختيار الزبون
        ttk.Label(self.content_frame, text="اختر الزبون:").pack(anchor=tk.E, padx=20)
        customers = self.db.get_all_customers()
        
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(self.content_frame, textvariable=customer_var,
                                      width=30, state='readonly')
        customer_combo['values'] = [f"{c[1]} (ID: {c[0]})" for c in customers]
        customer_combo.pack(anchor=tk.E, padx=20, pady=5)
        
        # منطقة العرض
        tree_frame = ttk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # جدول الفواتير
        tree = ttk.Treeview(tree_frame, columns=('المتر', 'السعر', 'الإجمالي', 'المدفوع', 'المتبقي'),
                           height=10)
        tree.column('#0', width=60, anchor=tk.CENTER)
        tree.column('المتر', width=80, anchor=tk.CENTER)
        tree.column('السعر', width=80, anchor=tk.CENTER)
        tree.column('الإجمالي', width=100, anchor=tk.CENTER)
        tree.column('المدفوع', width=100, anchor=tk.CENTER)
        tree.column('المتبقي', width=100, anchor=tk.CENTER)
        
        tree.heading('#0', text='رقم الفاتورة')
        tree.heading('المتر', text='الأمتار')
        tree.heading('السعر', text='السعر/م')
        tree.heading('الإجمالي', text='المبلغ الإجمالي')
        tree.heading('المدفوع', text='المدفوع')
        tree.heading('المتبقي', text='المتبقي')
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        def show_statement():
            try:
                customer_id = int(customer_var.get().split("ID: ")[1].rstrip(")"))
                customer_name, invoices = self.db.get_customer_statement(customer_id)
                
                # مسح الجدول السابق
                for item in tree.get_children():
                    tree.delete(item)
                
                total_balance = 0
                for inv in invoices:
                    total_balance += inv[5]  # المتبقي
                    tree.insert('', tk.END, text=f"#{inv[0]}",
                              values=(f"{inv[1]:.2f}", f"{inv[2]:.2f}", 
                                    f"{inv[3]:.2f}", f"{inv[4]:.2f}", 
                                    f"{inv[5]:.2f}"))
                
                # عرض الإجمالي
                summary_label.config(text=f"إجمالي المتبقي: {total_balance:.2f}")
            except:
                messagebox.showerror("خطأ", "اختر زبون صحيح")
        
        ttk.Button(self.content_frame, text="🔍 عرض البيان", 
                  command=show_statement).pack(pady=10)
        
        summary_label = ttk.Label(self.content_frame, text="إجمالي المتبقي: 0.00",
                                 font=("Arial", 12, "bold"))
        summary_label.pack(pady=10)
    
    def show_all_invoices(self):
        """عرض جميع الفواتير"""
        self.clear_content()
        
        ttk.Label(self.content_frame, text="جميع الفواتير", 
                 font=("Arial", 14, "bold")).pack(pady=10)
        
        tree_frame = ttk.Frame(self.content_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(tree_frame, 
                           columns=('الزبون', 'المتر', 'السعر', 'الإجمالي', 'المدفوع', 'المتبقي'),
                           height=15)
        tree.column('#0', width=60, anchor=tk.CENTER)
        tree.column('الزبون', width=100, anchor=tk.CENTER)
        tree.column('المتر', width=80, anchor=tk.CENTER)
        tree.column('السعر', width=80, anchor=tk.CENTER)
        tree.column('الإجمالي', width=100, anchor=tk.CENTER)
        tree.column('المدفوع', width=100, anchor=tk.CENTER)
        tree.column('المتبقي', width=100, anchor=tk.CENTER)
        
        tree.heading('#0', text='#')
        tree.heading('الزبون', text='الزبون')
        tree.heading('المتر', text='الأمتار')
        tree.heading('السعر', text='السعر/م')
        tree.heading('الإجمالي', text='المبلغ')
        tree.heading('المدفوع', text='المدفوع')
        tree.heading('المتبقي', text='المتبقي')
        
        tree.pack(fill=tk.BOTH, expand=True)
        
        # جلب البيانات
        import sqlite3
        conn = sqlite3.connect(self.db.db_name)
        c = conn.cursor()
        c.execute('''SELECT i.id, c.name, i.meters, i.price_per_meter, 
                            i.total_amount, i.paid_amount, i.remaining_debt
                     FROM invoices i
                     JOIN customers c ON i.customer_id = c.id
                     ORDER BY i.id DESC''')
        invoices = c.fetchall()
        conn.close()
        
        for idx, inv in enumerate(invoices, 1):
            tree.insert('', tk.END, text=f"{idx}",
                       values=(inv[1], f"{inv[2]:.2f}", f"{inv[3]:.2f}",
                              f"{inv[4]:.2f}", f"{inv[5]:.2f}", f"{inv[6]:.2f}"))

if __name__ == "__main__":
    root = tk.Tk()
    app = AccountingApp(root)
    root.mainloop()
