from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import io

app = Flask(__name__)
app.secret_key = 'super-secret-key-for-flash-messages' # Required for flash

# --- Constants & Configuration ---
BLOOD_TYPE_Z = {
    'O': 43,
    'A': 49,
    'B': 53,
    'AB': 60
}

# --- Membership Functions ---

def get_age_membership(x):
    res = {'Fase1': 0.0, 'Fase2': 0.0, 'Fase3': 0.0, 'Fase4': 0.0, 'Fase5': 0.0}
    if x < 6: res['Fase1'] = 1.0
    elif 6 <= x <= 12: res['Fase1'] = (12 - x) / 6.0
    
    if 6 <= x <= 12: res['Fase2'] = (x - 6) / 6.0
    elif 12 <= x <= 24: res['Fase2'] = (24 - x) / 12.0
    
    if 12 <= x <= 24: res['Fase3'] = (x - 12) / 12.0
    elif 24 <= x <= 36: res['Fase3'] = (36 - x) / 12.0
    
    if 24 <= x <= 36: res['Fase4'] = (x - 24) / 12.0
    elif 36 <= x <= 48: res['Fase4'] = (48 - x) / 12.0
    
    if 36 <= x <= 48: res['Fase5'] = (x - 36) / 12.0
    elif x > 48: res['Fase5'] = 1.0
    
    return res

def get_weight_membership(x, gender):
    res = {'Light': 0.0, 'Medium': 0.0, 'Heavy': 0.0}
    gender = gender.upper()
    if gender == 'L':
        if x <= 7: res['Light'] = 1.0
        elif 7 < x <= 13: res['Light'] = (13 - x) / 6.0
        
        if 7 < x <= 13: res['Medium'] = (x - 7) / 6.0
        elif 13 < x <= 19: res['Medium'] = (19 - x) / 6.0
        
        if 13 < x <= 19: res['Heavy'] = (x - 13) / 6.0
        elif x > 19: res['Heavy'] = 1.0
    elif gender == 'P':
        if x <= 7: res['Light'] = 1.0
        elif 7 < x <= 12: res['Light'] = (12 - x) / 5.0
        
        if 7 < x <= 12: res['Medium'] = (x - 7) / 5.0
        elif 12 < x <= 18: res['Medium'] = (18 - x) / 6.0
        
        if 12 < x <= 18: res['Heavy'] = (x - 12) / 6.0
        elif x > 18: res['Heavy'] = 1.0
    return res

def classify_result(score):
    if score <= 42: return "Normal (Obesitas Buruk)"
    elif 42 < score <= 51: return "Obesitas Kurang"
    elif 51 < score <= 56.5: return "Obesitas Sedang"
    elif 56.5 < score <= 65: return "Obesitas Baik"
    else: return "Out of Range"

def calculate_sugeno_score(age, weight, gender, blood_type):
    age_mf = get_age_membership(age)
    weight_mf = get_weight_membership(weight, gender)
    z_val = BLOOD_TYPE_Z.get(blood_type.upper(), 0)
    
    numerator = 0.0
    denominator = 0.0
    
    for age_score in age_mf.values():
        if age_score == 0: continue
        for weight_score in weight_mf.values():
            if weight_score == 0: continue
            alpha = min(age_score, weight_score)
            numerator += alpha * z_val
            denominator += alpha
            
    if denominator == 0: return 0.0
    return numerator / denominator

# --- Routes ---

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', result_type=None)

@app.route('/process_manual', methods=['POST'])
def process_manual():
    try:
        name = request.form['name']
        age = float(request.form['age'])
        weight = float(request.form['weight'])
        gender = request.form['gender']
        blood_type = request.form['blood_type']
        
        score = calculate_sugeno_score(age, weight, gender, blood_type)
        category = classify_result(score)
        
        result = {'name': name, 'score': score, 'category': category}
        return render_template('index.html', result=result, result_type='manual')
    except Exception as e:
        flash(f"Input Error: {str(e)}", "error")
        return redirect(url_for('index'))

@app.route('/process_csv', methods=['POST'])
def process_csv():
    if 'file' not in request.files:
        flash("File tidak ditemukan", "error")
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash("Belum ada file yang dipilih", "error")
        return redirect(url_for('index'))
    
    if file:
        results = []
        try:
            # 1. Read file content as string
            stream = io.TextIOWrapper(file.stream._file, encoding='utf-8-sig', errors='replace')
            content = stream.read()
            
            # 2. Sniff delimiter (Comma or Semicolon)
            # Fallback to comma if detection fails
            try:
                dialect = csv.Sniffer().sniff(content[:1024])
                delimiter = dialect.delimiter
            except csv.Error:
                delimiter = ',' # Default fallback
                
            # Force semicolon if it seems more prevalent in the first line (common in Indo Excel)
            first_line = content.splitlines()[0] if content else ''
            if first_line.count(';') > first_line.count(','):
                delimiter = ';'

            # 3. Parse CSV
            stream.seek(0)
            csv_input = csv.DictReader(stream, delimiter=delimiter)
            
            # 4. Process Rows
            if not csv_input.fieldnames:
                 flash("File CSV kosong", "error")
                 return redirect(url_for('index'))
                 
            # Normalize headers for mapping
            headers_map = {h.strip().lower(): h for h in csv_input.fieldnames}
            
            # Helper to find column loosely
            def get_col(candidates):
                for c in candidates:
                    if c in headers_map:
                        return headers_map[c]
                return None

            col_name = get_col(['nama', 'name', 'nama anak', 'nama_anak', 'nama lengkap'])
            col_age = get_col(['usia', 'age', 'umur', 'bulan', 'usia (bulan)'])
            col_weight = get_col(['bb', 'berat', 'weight', 'berat badan', 'berat_badan'])
            col_gender = get_col(['gender', 'jk', 'jenis kelamin', 'sex', 'l/p', 'l / p', 'p/l'])
            col_blood = get_col(['goldar', 'golongan darah', 'blood', 'blood type', 'gol darah', 'gol. darah'])
            
            if not (col_name and col_age and col_weight):
                found_cols = [k for k in headers_map.keys()]
                flash(f"Format Kolom tidak dikenali. Kolom wajib: Nama, Usia, BB. (Ditemukan: {found_cols})", "error")
                return redirect(url_for('index'))
            
            # Prepare Headers for Display (Original + New Cols)
            display_headers = csv_input.fieldnames + ['Skor Sugeno', 'Kategori Gizi']

            for row in csv_input:
                try:
                    name = row[col_name].strip()
                    if not name: continue
                    
                    # Handle comma decimals (e.g. "12,5" -> 12.5) for Indonesia
                    age_raw = row[col_age].replace(',', '.')
                    weight_raw = row[col_weight].replace(',', '.')
                    
                    age = float(age_raw)
                    weight = float(weight_raw)
                    
                    gender = row.get(col_gender, 'L').strip() if col_gender else 'L'
                    
                    # Handle Blood Type '0' (zero) -> 'O' (letter) common typo
                    blood_raw = row.get(col_blood, 'O').strip().upper() if col_blood else 'O'
                    if blood_raw == '0': 
                        blood_type = 'O'
                    else:
                        blood_type = blood_raw
                    
                    score = calculate_sugeno_score(age, weight, gender, blood_type)
                    category = classify_result(score)
                    
                    # Copy original row and add results
                    row_data = row.copy()
                    row_data['Skor Sugeno'] = score
                    row_data['Kategori Gizi'] = category
                    
                    results.append(row_data)

                except (ValueError, KeyError):
                    continue 

            if not results:
                 flash("Tidak ada data yang valid untuk diproses.", "warning")

            # Force tab switch via template variable or JS logic (optional, but good UX)
            return render_template('index.html', results=results, headers=display_headers, result_type='csv')
            
        except Exception as e:
             flash(f"Error sistem: {str(e)}", "error")
             return redirect(url_for('index'))

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
