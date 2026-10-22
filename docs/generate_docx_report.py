import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_background(cell, fill_hex):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders_xml = f'''
    <w:tblBorders {nsdecls("w")}>
        <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
    </w:tblBorders>
    '''
    tblPr.append(parse_xml(borders_xml))

def build_docx_report():
    doc = Document()

    # Set page margins to 0.75 in
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # -------------------------------------------------------------
    # PAGE 1: ASSIGNMENT FRONT SHEET
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("KARPAGAM COLLEGE OF ENGINEERING\n")
    r_inst.bold = True
    r_inst.font.size = Pt(14)
    r_inst.font.name = "Arial"
    r_inst.font.color.rgb = RGBColor(179, 39, 35)

    r_sub = p_inst.add_run("Rediscover | Refine | Redefine\nAccredited by NAAC with 'A+' Grade | Autonomous Institution | Affiliated to Anna University\n")
    r_sub.font.size = Pt(8.5)
    r_sub.font.color.rgb = RGBColor(100, 100, 100)

    p_ay = doc.add_paragraph()
    p_ay.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ay = p_ay.add_run("ACADEMIC YEAR: 2026-27\n")
    r_ay.bold = True
    r_ay.font.size = Pt(11)

    r_fs = p_ay.add_run("ASSIGNMENT FRONT SHEET")
    r_fs.bold = True
    r_fs.font.size = Pt(13)

    # Table for Front Sheet Details
    table = doc.add_table(rows=9, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    set_table_borders(table, color="333333", sz="8")

    col_widths = [Inches(2.5), Inches(4.5)]
    front_data = [
        ("Name of the Student:", "Cibi K."),
        ("Register Number:", "717825F112"),
        ("Course Code & Title:", "23CSR306 JAVA PROGRAMMING"),
        ("Year / Dept. / Sem / Section:", "II / IT / III / A"),
        ("Assignment:", "II – OOP Mini Project (any one of 35)"),
        ("Specification No. & Title:", "Specification 2: Library Management System"),
        ("GitHub Repository Link:", "https://github.com/cibi-k/LibraryManagementSystem-JAVA"),
        ("Date of Issue:", "06-10-2026"),
        ("Date of Submission:", "")
    ]

    for idx, (label, val) in enumerate(front_data):
        row = table.rows[idx]
        cell_lbl = row.cells[0]
        cell_val = row.cells[1]
        cell_lbl.width = col_widths[0]
        cell_val.width = col_widths[1]
        set_cell_margins(cell_lbl, 100, 100, 120, 120)
        set_cell_margins(cell_val, 100, 100, 120, 120)
        set_cell_background(cell_lbl, "F0F4F8")

        p0 = cell_lbl.paragraphs[0]
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.size = Pt(10)
        r0.font.name = "Arial"

        p1 = cell_val.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(10)
        r1.font.name = "Arial"
        if "github.com" in val:
            r1.font.color.rgb = RGBColor(0, 102, 204)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Marks Details Table
    p_md = doc.add_paragraph()
    r_md = p_md.add_run("Marks Details")
    r_md.bold = True
    r_md.font.size = Pt(11)

    marks_table = doc.add_table(rows=4, cols=3)
    marks_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(marks_table, color="333333", sz="8")
    m_widths = [Inches(2.5), Inches(2.2), Inches(2.3)]

    m_rows = [
        ("CO / K Level", "Maximum Marks", "Marks Obtained"),
        ("CO4 / K3", "50", ""),
        ("CO5 / K3", "50", ""),
        ("Total", "100", "")
    ]

    for r_idx, row_data in enumerate(m_rows):
        row = marks_table.rows[r_idx]
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = m_widths[c_idx]
            set_cell_margins(cell, 120, 120, 120, 120)
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Arial"
            r.font.size = Pt(10)
            if r_idx == 0 or r_idx == 3:
                r.bold = True
                set_cell_background(cell, "E2E8F0")

    doc.add_paragraph().paragraph_format.space_after = Pt(24)
    p_sign = doc.add_paragraph()
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sign = p_sign.add_run("Course In-charge Signature: _______________________")
    r_sign.bold = True
    r_sign.font.size = Pt(10)

    # -------------------------------------------------------------
    # PAGE 2: EVALUATION RUBRICS
    # -------------------------------------------------------------
    doc.add_page_break()

    p_rub_title = doc.add_paragraph()
    p_rub_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rt = p_rub_title.add_run("Rubrics for Assignment Evaluation\n")
    r_rt.bold = True
    r_rt.font.size = Pt(13)

    # Info table above rubrics
    info_tbl = doc.add_table(rows=3, cols=4)
    info_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(info_tbl, color="666666", sz="4")
    it_data = [
        ("Assignment Number:", "II", "Date:", "06-10-2026"),
        ("Course Code & Title:", "23CSR306 Java Programming", "Specification No. & Title:", "Specification 2: Library Management System"),
        ("Register Number:", "717825F112", "Name of the Student:", "Cibi K.")
    ]
    for r_idx, row in enumerate(it_data):
        for c_idx, text in enumerate(row):
            cell = info_tbl.rows[r_idx].cells[c_idx]
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.size = Pt(9)
            r.font.name = "Arial"
            if c_idx % 2 == 0:
                r.bold = True
                set_cell_background(cell, "F5F5F5")

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    p_rub_sub = doc.add_paragraph()
    r_rsub = p_rub_sub.add_run("Marks for each criterion = Level (1 – 5) × Weightage. Total: 100 (CO4: 50 + CO5: 50).")
    r_rsub.font.size = Pt(9)
    r_rsub.italic = True

    # Rubrics Detail Table
    rub_tbl = doc.add_table(rows=8, cols=9)
    rub_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(rub_tbl, color="666666", sz="4")

    headers = ["Criterion", "CO", "Wt.", "Exemplary (5)", "Excellent (4)", "Adequate (3)", "Average (2)", "Inadequate (1)", "Max"]
    r_widths = [Inches(1.2), Inches(0.4), Inches(0.35), Inches(1.3), Inches(1.1), Inches(1.0), Inches(0.9), Inches(0.85), Inches(0.4)]

    for c_idx, h in enumerate(headers):
        cell = rub_tbl.rows[0].cells[c_idx]
        set_cell_background(cell, "D9E1F2")
        set_cell_margins(cell, 80, 80, 60, 60)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.size = Pt(8)
        r.font.name = "Arial"

    rubric_rows = [
        ("Program Correctness & Business Rules", "CO4", "4", "All menu options work; every business rule enforced correctly.", "All options work; minor gaps in one rule.", "Main flow works; some rules missing.", "Partially working; several rules not handled.", "Does not run or most features missing.", "20"),
        ("Input Validation & Exception Handling", "CO4", "3", "All inputs validated; custom exceptions; program never crashes.", "Most inputs validated with try-catch.", "Basic validation; some invalid inputs not handled.", "Little validation; crashes on bad input.", "No validation or exception handling.", "15"),
        ("Menu-driven Interface & Expected Outputs", "CO4", "3", "Clear menu; all expected outputs (receipts/status) shown neatly.", "Clear menu; most expected outputs shown.", "Menu works; outputs basic or incomplete.", "Menu unclear; few outputs shown.", "No proper menu or outputs.", "15"),
        ("OOP Design (Encapsulation, Inheritance, Aggregation, Polymorphism)", "CO5", "4", "All four concepts applied meaningfully; all required classes present.", "Concepts applied well; minor design gaps.", "Classes present; concepts used in a basic way.", "Weak design; some required classes missing.", "No OOP design; mostly procedural.", "20"),
        ("Code Quality & Package Structure", "CO5", "2", "Clean packages, naming, indentation and comments.", "Good structure with few lapses.", "Acceptable structure; average readability.", "Poor naming / structure.", "Single file; unreadable code.", "10"),
        ("GitHub Repository & README", "CO5", "1", "Complete code with clear README (problem, run steps, name, roll no.).", "Complete code; README missing minor details.", "Code present; README incomplete.", "Partial code; no README.", "No repository.", "5"),
        ("Viva / Explanation", "CO5", "3", "Explains design, rules and code clearly; answers all questions.", "Explains well; answers most questions.", "Explains main logic; answers some questions.", "Limited explanation of own code.", "Unable to explain code.", "15")
    ]

    for r_idx, r_data in enumerate(rubric_rows):
        row = rub_tbl.rows[r_idx + 1]
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            set_cell_margins(cell, 60, 60, 50, 50)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(7.5)
            r.font.name = "Arial"
            if c_idx in [1, 2, 8]:
                r.bold = True
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph().paragraph_format.space_after = Pt(16)
    p_sig2 = doc.add_paragraph()
    r_sig2 = p_sig2.add_run("CO4 Total (Criteria 1 – 3): 50   |   CO5 Total (Criteria 4 – 7): 50   |   Total Marks: 100\n\nSignature of the Evaluator with date: _______________________________")
    r_sig2.bold = True
    r_sig2.font.size = Pt(9.5)

    # -------------------------------------------------------------
    # PAGE 3: SUBMISSION TEMPLATE & SECTIONS 1 - 5
    # -------------------------------------------------------------
    doc.add_page_break()

    # Header block
    p_th = doc.add_paragraph()
    r_th1 = p_th.add_run("Department of Computer Science and Engineering\n")
    r_th1.bold = True
    r_th1.font.size = Pt(11)
    r_th2 = p_th.add_run("Reg. No: 717825F112              Name: Cibi K.              Assignment II Report\n")
    r_th2.font.size = Pt(9.5)
    r_th2.italic = True

    p_tt = doc.add_paragraph()
    p_tt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_tt = p_tt.add_run("23CSR306 JAVA PROGRAMMING\nAssignment – II Submission Template\n")
    r_tt.bold = True
    r_tt.font.size = Pt(12)

    p_spec = doc.add_paragraph()
    r_spec = p_spec.add_run("Specification No. & Title: Specification 2: Library Management System")
    r_spec.bold = True
    r_spec.font.size = Pt(11)
    p_spec.paragraph_format.space_after = Pt(12)

    # =============================================================
    # 1. ASSIGNMENT QUESTION (Verbatim from Question PDF)
    # =============================================================
    p_q_head = doc.add_paragraph()
    r_qh = p_q_head.add_run("1. Assignment Question")
    r_qh.bold = True
    r_qh.font.size = Pt(12)
    r_qh.font.color.rgb = RGBColor(0, 51, 102)

    q_box = doc.add_table(rows=1, cols=1)
    q_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(q_box, color="003366", sz="8")
    cell_q = q_box.rows[0].cells[0]
    cell_q.width = Inches(7.0)
    set_cell_background(cell_q, "F8F9FA")
    set_cell_margins(cell_q, 150, 150, 180, 180)

    p_qb = cell_q.paragraphs[0]
    r_ps_title = p_qb.add_run("Specification 2: Library Management System\n\n")
    r_ps_title.bold = True
    r_ps_title.font.size = Pt(11)

    r_ps_lbl = p_qb.add_run("Problem Statement: ")
    r_ps_lbl.bold = True
    p_qb.add_run("Design and implement a Java console application for a Library Management System that manages books, members, borrowing, and returns. The system should follow object-oriented principles and ensure proper tracking of availability.\n\n")

    r_cr_lbl = p_qb.add_run("Class Requirements: ")
    r_cr_lbl.bold = True
    p_qb.add_run("Book, Author, Member, PremiumMember, BorrowTransaction, ReturnTransaction, Library\n\n")

    r_br_lbl = p_qb.add_run("Business Rules:\n")
    r_br_lbl.bold = True
    p_qb.add_run("1. Books can only be borrowed if they are available in stock.\n"
                 "2. When borrowed, stock reduces; when returned, stock updates.\n"
                 "3. Premium members may borrow more books and for longer duration.\n"
                 "4. Fines are applied for late returns.\n"
                 "5. Borrowing and returning transactions must link directly to books.\n\n")

    r_mo_lbl = p_qb.add_run("Menu Options: ")
    r_mo_lbl.bold = True
    p_qb.add_run("Add Book / Add Member / Borrow Book / Return Book / Display Available Books / Exit\n\n")

    r_eo_lbl = p_qb.add_run("Expected Output:\n")
    r_eo_lbl.bold = True
    p_qb.add_run("• Show borrow/return receipt.\n"
                 "• Display updated stock after each transaction.\n"
                 "• Show fines (if applicable).\n")

    doc.add_paragraph().paragraph_format.space_after = Pt(14)

    # =============================================================
    # 2. JAVA SOURCE CODE
    # =============================================================
    p_code_head = doc.add_paragraph()
    r_ch = p_code_head.add_run("2. Java Source Code")
    r_ch.bold = True
    r_ch.font.size = Pt(12)
    r_ch.font.color.rgb = RGBColor(0, 51, 102)

    p_code_note = doc.add_paragraph()
    r_cn = p_code_note.add_run("(Complete source code organized package by package – model, service, util, exception, main, test. Font: Consolas, 9.5 pt, syntax preserved)")
    r_cn.font.size = Pt(9)
    r_cn.italic = True
    p_code_note.paragraph_format.space_after = Pt(10)

    # Define all source files to include
    src_base = r"C:\Users\kcibi\.gemini\antigravity\scratch\LibraryManagementSystem-JAVA\src"
    source_files = [
        ("model/Author.java", os.path.join(src_base, "com", "library", "model", "Author.java")),
        ("model/Book.java", os.path.join(src_base, "com", "library", "model", "Book.java")),
        ("model/Member.java", os.path.join(src_base, "com", "library", "model", "Member.java")),
        ("model/PremiumMember.java", os.path.join(src_base, "com", "library", "model", "PremiumMember.java")),
        ("model/BorrowTransaction.java", os.path.join(src_base, "com", "library", "model", "BorrowTransaction.java")),
        ("model/ReturnTransaction.java", os.path.join(src_base, "com", "library", "model", "ReturnTransaction.java")),
        ("exception/LibraryException.java", os.path.join(src_base, "com", "library", "exception", "LibraryException.java")),
        ("exception/BookNotFoundException.java", os.path.join(src_base, "com", "library", "exception", "BookNotFoundException.java")),
        ("exception/MemberNotFoundException.java", os.path.join(src_base, "com", "library", "exception", "MemberNotFoundException.java")),
        ("exception/InsufficientStockException.java", os.path.join(src_base, "com", "library", "exception", "InsufficientStockException.java")),
        ("exception/BorrowLimitExceededException.java", os.path.join(src_base, "com", "library", "exception", "BorrowLimitExceededException.java")),
        ("exception/InvalidTransactionException.java", os.path.join(src_base, "com", "library", "exception", "InvalidTransactionException.java")),
        ("exception/DuplicateEntityException.java", os.path.join(src_base, "com", "library", "exception", "DuplicateEntityException.java")),
        ("service/Library.java", os.path.join(src_base, "com", "library", "service", "Library.java")),
        ("util/ValidationUtil.java", os.path.join(src_base, "com", "library", "util", "ValidationUtil.java")),
        ("main/Main.java", os.path.join(src_base, "com", "library", "main", "Main.java")),
        ("test/LibrarySystemTest.java", os.path.join(src_base, "com", "library", "test", "LibrarySystemTest.java")),
    ]

    for display_path, abs_path in source_files:
        p_sub = doc.add_paragraph()
        p_sub.paragraph_format.space_before = Pt(12)
        p_sub.paragraph_format.space_after = Pt(4)
        r_sub = p_sub.add_run(f"File: src/com/library/{display_path}")
        r_sub.bold = True
        r_sub.font.size = Pt(10.5)
        r_sub.font.color.rgb = RGBColor(0, 102, 153)

        if os.path.exists(abs_path):
            with open(abs_path, "r", encoding="utf-8") as f:
                code_content = f.read()
        else:
            code_content = f"// File not found: {abs_path}"

        # Code block container table
        tbl_code = doc.add_table(rows=1, cols=1)
        tbl_code.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(tbl_code, color="D0D7DE", sz="4")
        cell_c = tbl_code.rows[0].cells[0]
        cell_c.width = Inches(7.0)
        set_cell_background(cell_c, "F6F8FA")
        set_cell_margins(cell_c, 100, 100, 120, 120)

        p_cp = cell_c.paragraphs[0]
        p_cp.paragraph_format.space_before = Pt(0)
        p_cp.paragraph_format.space_after = Pt(0)
        p_cp.paragraph_format.line_spacing = Pt(11)
        r_code = p_cp.add_run(code_content)
        r_code.font.name = "Consolas"
        r_code.font.size = Pt(8.5)
        r_code.font.color.rgb = RGBColor(36, 41, 47)

    # =============================================================
    # 3. EXECUTION OUTPUT SCREENSHOTS
    # =============================================================
    doc.add_page_break()
    p_scr_head = doc.add_paragraph()
    r_sh = p_scr_head.add_run("3. Execution Output Screenshots")
    r_sh.bold = True
    r_sh.font.size = Pt(12)
    r_sh.font.color.rgb = RGBColor(0, 51, 102)

    p_scr_desc = doc.add_paragraph()
    r_sd = p_scr_desc.add_run("Execution outputs captured directly from program execution in the project environment. Each screenshot verifies key requirements from Specification 2, including Main Menu display, Input Validation, Borrowing Receipt, Updated Stock, and Late Fine calculation.")
    r_sd.font.size = Pt(9.5)

    screenshots = [
        ("screenshots/screen_01_main_menu.png", "Figure 1: Main menu display showing all 6 required options and header details."),
        ("screenshots/screen_02_add_book_and_member.png", "Figure 2: Successfully adding new Book (BK-105) and registering Regular and Premium members."),
        ("screenshots/screen_03_borrow_receipt.png", "Figure 3: Official borrow receipt generation showing 14-day due date and immediately updated stock (2 -> 1)."),
        ("screenshots/screen_04_premium_and_stock_validation.png", "Figure 4: Premium member extended loan (30 days) and rejection of borrowing when book stock is 0/1."),
        ("screenshots/screen_05_return_ontime_receipt.png", "Figure 5: On-time book return receipt, stock restored (1 -> 2), with zero fine (Rs. 0.00)."),
        ("screenshots/screen_06_return_overdue_fine.png", "Figure 6: Return receipt showing overdue fine calculation (10 days @ Rs.5/day = Rs.50.00) and unborrowed/duplicate return rejection."),
        ("screenshots/screen_07_display_available_books.png", "Figure 7: Display Available Books table and validation handling of invalid menu choices without crashing."),
    ]

    base_dir = r"C:\Users\kcibi\.gemini\antigravity\scratch\LibraryManagementSystem-JAVA"
    for img_rel, caption in screenshots:
        img_abs = os.path.join(base_dir, img_rel)
        if os.path.exists(img_abs):
            doc.add_paragraph().paragraph_format.space_before = Pt(8)
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(2)
            doc.add_picture(img_abs, width=Inches(6.6))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(10)
            r_cap = p_cap.add_run(caption)
            r_cap.font.size = Pt(9)
            r_cap.italic = True
            r_cap.font.color.rgb = RGBColor(50, 50, 50)

    # Eclipse reproduction instructions note
    p_ec_note = doc.add_paragraph()
    p_ec_note.paragraph_format.space_before = Pt(12)
    r_en = p_ec_note.add_run("Note on Capturing in Eclipse IDE:\n")
    r_en.bold = True
    r_en.font.size = Pt(10)
    p_ec_note.add_run("To reproduce and capture these identical console outputs directly inside Eclipse IDE:\n"
                     "1. Import project via File -> Import... -> General -> Existing Projects into Workspace.\n"
                     "2. Run Main.java by right-clicking -> Run As -> Java Application.\n"
                     "3. Execute the respective menu commands (1 through 6) in the Eclipse Console tab at the bottom.\n"
                     "4. Use Alt + PrtScn or Windows Snipping Tool (Win + Shift + S) to capture the Eclipse Console window.\n")

    # =============================================================
    # 4. GITHUB REPOSITORY LINK & DETAILS
    # =============================================================
    doc.add_page_break()
    p_gh_head = doc.add_paragraph()
    r_gh = p_gh_head.add_run("4. GitHub Repository Link")
    r_gh.bold = True
    r_gh.font.size = Pt(12)
    r_gh.font.color.rgb = RGBColor(0, 51, 102)

    tbl_gh = doc.add_table(rows=5, cols=2)
    tbl_gh.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl_gh, color="003366", sz="6")
    tbl_gh.rows[0].cells[0].width = Inches(2.2)
    tbl_gh.rows[0].cells[1].width = Inches(4.8)

    gh_info = [
        ("Repository URL:", "https://github.com/cibi-k/LibraryManagementSystem-JAVA"),
        ("Repository Name:", "LibraryManagementSystem-JAVA"),
        ("Author / Student:", "Cibi K. (Register No: 717825F112)"),
        ("Branch:", "main"),
        ("README.md Contents:", "Problem statement, business rules, OOP architecture, JDK 17 setup, Eclipse import steps, CLI commands, verified 17-scenario test matrix, fine & loan policies.")
    ]

    for idx, (label, val) in enumerate(gh_info):
        row = tbl_gh.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.8)
        set_cell_margins(c0, 100, 100, 120, 120)
        set_cell_margins(c1, 100, 100, 120, 120)
        set_cell_background(c0, "F0F4F8")

        p0 = c0.paragraphs[0]
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.size = Pt(9.5)
        r0.font.name = "Arial"

        p1 = c1.paragraphs[0]
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)
        r1.font.name = "Arial"
        if "github.com" in val:
            r1.font.color.rgb = RGBColor(0, 102, 204)
            r1.bold = True

    output_path = os.path.join(base_dir, "docs", "23CSR306_Assignment_II_Report_717825F112.docx")
    doc.save(output_path)
    print(f"Report DOCX saved successfully at: {output_path}")

if __name__ == "__main__":
    build_docx_report()
