Power BI Portfolio — Financial Performance & Customer Risk Dashboards

Bu repo, iki farklı iş senaryosu için hazırlanmış Power BI raporlarını ve raporlarda kullanılan veri üretim script’lerini içerir:

Financial Performance Dashboard

Customer Risk Dashboard

Amaç; yönetim seviyesinde takip edilen temel performans göstergelerini, detay seviyesinde operasyonel analizi ve kullanıcı dostu etkileşimli bir veri modeli sunmaktır.

Veri Modeli

Proje, star-schema mantığında aşağıdaki tablolardan oluşur:

Dimension Tabloları

dimDate

dimBranch

dimProduct

dimCustomer

Fact Tabloları

factFinancials

factTransactions

factDataLoad

Tüm fact tabloları ilgili dimension tabloları ile anahtar kolonlar (DateKey, BranchKey, ProductKey, ProductID, CustomerID) üzerinden ilişkilendirilmiştir.

Data Generator (Python)

Veriler, Python ile yazılmış veri üretim script’i kullanılarak oluşturulmuştur.
Script, gerçek ticari davranışları taklit eden rastgele ancak tutarlı kayıtlar oluşturur.

Üretim Mantığı

dimDate → 2023–2025 takvimini günlük bazda üretir.

dimBranch → Türkiye’de çeşitli şehir ve bölge yapısına göre şube listesi oluşturur.

dimProduct → Bankacılık ve finans ürün kategorilerini içerir.

dimCustomer → Müşteri tipi, şehir ve segment bilgisini içerir.

factFinancials → Her gün, şube ve ürün bazlı gelir/gider/işlem hacmi üretir.

factTransactions → Müşterilerin yaptığı işlemleri, tutar, kanal, işlem tipi ve olası şüpheli davranış bayraklarıyla üretir.

factDataLoad → Veri yükleme süreçleriyle ilgili kayıtlar üretir (record count, errors, duration, status).

Bu yaklaşım, Power BI raporlarının gerçek veri davranışına yakın şekilde test edilmesine olanak sağlar.

Financial Performance Dashboard

Bu sayfa, işletmenin finansal durumunu aylık ve kategorik bazda takip etmeyi amaçlar.

Yer alan metrikler:

Toplam Gelir (Total Revenue)

Toplam Gider (Total Expense)

Toplam Kâr (Total Profit)

Kâr Marjı (Profit Margin)

Aylık Gelir/Gider Trendleri

MoM Revenue Growth %

Şube Bazlı Revenue

Ürün Bazlı Revenue Dağılımı

Dashboard, yıl, ürün kategorisi, şehir ve bölge filtreleri ile etkileşimlidir.

Customer Risk Dashboard

Bu sayfa, müşteri işlemlerine ilişkin olağan dışı davranışları tespit etmeye yönelik görseller içerir.

Yer alan metrikler:

Toplam İşlem Sayısı

İşaretlenmiş (Flagged) İşlem Sayısı

Flagged Transaction %

İşlem Kanalı ve Türüne Göre Dağılım

Müşteri Bazlı Risk Görünümü

Bu dashboard, güvenlik ve risk operasyonlarının ihtiyaç duyduğu göstergeleri sağlar.

Kullanılan DAX Measures
Finansal Metrikler
Total Revenue = SUM(factFinancials[Revenue])

Total Expense = SUM(factFinancials[Expense])

Total Profit = [Total Revenue] - [Total Expense]

Profit Margin = DIVIDE([Total Profit], [Total Revenue])

MoM Revenue Growth
MoM Revenue Growth % =
VAR Curr = [Total Revenue]
VAR Prev = CALCULATE([Total Revenue], DATEADD(dimDate[Date], -1, MONTH))
RETURN
    DIVIDE(Curr - Prev, Prev)

YoY Revenue Growth
YoY Revenue Growth % =
VAR Curr = [Total Revenue]
VAR PrevYear =
    CALCULATE([Total Revenue], DATEADD(dimDate[Date], -1, YEAR))
RETURN
    DIVIDE(Curr - PrevYear, PrevYear)

Customer Risk Metrikleri
Total Transactions = COUNTROWS(factTransactions)

Flagged Transactions =
CALCULATE(
    COUNTROWS(factTransactions),
    factTransactions[IsFlagged] = 1
)

Flagged Transactions % =
DIVIDE([Flagged Transactions], [Total Transactions])
