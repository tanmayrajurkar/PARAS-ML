from supabase import create_client

SUPABASE_URL = "https://ipmshfkymnflueddojcw.supabase.co"
SUPABASE_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlwbXNoZmt5bW5mbHVlZGRvamN3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzE5NDU0NzAsImV4cCI6MjA0NzUyMTQ3MH0.CIAqAEJ_aV5OIbyCKEShSljutfYdmGR67tvpVgO1gUc"

supabase = create_client(SUPABASE_URL, SUPABASE_API_KEY)
