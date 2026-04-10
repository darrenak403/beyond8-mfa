from sqlalchemy import create_engine

# Dán chuỗi đã sửa vào đây
url = "postgresql+psycopg2://postgres.uyhzaxldnpvodqafgzct:Ngothanhdat%404002@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"

try:
    engine = create_engine(url)
    connection = engine.connect()
    print("🚀 Kết nối Supabase thành công!")
    connection.close()
except Exception as e:
    print(f"❌ Lỗi rồi: {e}")