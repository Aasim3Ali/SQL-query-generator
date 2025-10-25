import re
from typing import Optional
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

def enforce_coverage_pattern(query:str,table_name:str,column_names:str,value:Optional[str]=None)->str:
    queryL=query.lower()
    if "coverage" in queryL:
        for col in column_names:
            if col.lower() in queryL:
                tgt_col=col
                break
        if not tgt_col:
            tgt_col="SDC_FILENAME"
        
        if value==None:
            fixed_query = f"""
            SELECT
            {tgt_col},
            COUNT(CASE WHEN status = 'passed' THEN 1 END) * 1.0 / COUNT(*) AS coverage
            FROM {table_name}
            GROUP BY {tgt_col};
            """.strip()
            return fixed_query
        else:
            fixed_query = f"""
            SELECT
            {tgt_col},
            COUNT(CASE WHEN LOWER(status) = 'passed' and LOWER({tgt_col})=LOWER({value}) THEN 1 END) * 1.0 / COUNT(* where LOWER({tgt_col})=LOWER({value})) AS coverage
            FROM {table_name}
            """.strip()
            return fixed_query
    return query