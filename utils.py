import re

def extract_sql_query(text:str)->str:
    if not text:
        return ""
    cleaned=re.sub(r"```sql|```", "", text, flags=re.IGNORECASE).strip()
    match=re.search(r"\b(SELECT|INSERT|UPDATE|DELETE)\b", cleaned, re.IGNORECASE)
    if match:
        cleaned=cleaned[match.start():].strip()
    semi=cleaned.find(';')
    if semi!=-1:
        cleaned=cleaned[:semi+1]
    return cleaned.strip()

def get_schema(data,sample_size=5):
    schema={}
    for key in data[0].keys():
        values=[row.get(key) for row in data[:sample_size] if row.get(key)]
        default_type="string"
        for v in values:
            if isinstance(v,(int,float)):
                default_type="numeric"
                break
            if isinstance(v,str) and v.replace(".","",1).isdigit():
                default_type="numeric"
                break
        schema[key]=default_type
    return schema
