import os
import reportlab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, Preformatted
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self._pageNumber > 2:  # Start page numbers on page 3
            self.saveState()
            self.setFont("Helvetica", 9)
            self.setFillColor(colors.HexColor("#555555"))
            page_text = f"Page {self._pageNumber} of {page_count}"
            self.drawRightString(612 - 45, 25, page_text)
            header_text = "23CSR306 Java Programming | Reg: 717825F112 | Cibi K."
            self.drawString(45, 792 - 25, header_text)
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(45, 792 - 28, 612 - 45, 792 - 28)
            self.restoreState()

def build_pdf_report():
    pdf_path = r"C:\Users\kcibi\.gemini\antigravity\scratch\LibraryManagementSystem-JAVA\docs\23CSR306_Assignment_II_Report_717825F112.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    inst_style = ParagraphStyle(
        'InstTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        alignment=1,
        textColor=colors.HexColor("#B32723")
    )
    inst_sub = ParagraphStyle(
        'InstSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        alignment=1,
        textColor=colors.HexColor("#555555")
    )
    title_bold = ParagraphStyle(
        'TitleBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        alignment=1
    )
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11
    )
    cell_norm = ParagraphStyle(
        'CellNorm',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11
    )
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#003366"),
        spaceBefore=10,
        spaceAfter=6
    )
    code_subheading = ParagraphStyle(
        'CodeSubHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#006699"),
        spaceBefore=8,
        spaceAfter=3
    )
    caption_style = ParagraphStyle(
        'CaptionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11,
        alignment=1,
        textColor=colors.HexColor("#333333"),
        spaceBefore=3,
        spaceAfter=10
    )

    story = []

    # =============================================================
    # PAGE 1: ASSIGNMENT FRONT SHEET
    # =============================================================
    story.append(Paragraph("KARPAGAM COLLEGE OF ENGINEERING", inst_style))
    story.append(Paragraph("Rediscover | Refine | Redefine<br/>Accredited by NAAC with 'A+' Grade | Autonomous Institution | Affiliated to Anna University", inst_sub))
    story.append(Spacer(1, 10))
    story.append(Paragraph("ACADEMIC YEAR: 2026-27<br/><b>ASSIGNMENT FRONT SHEET</b>", title_bold))
    story.append(Spacer(1, 12))

    front_table_data = [
        [Paragraph("Name of the Student:", cell_bold), Paragraph("Cibi K.", cell_norm)],
        [Paragraph("Register Number:", cell_bold), Paragraph("717825F112", cell_norm)],
        [Paragraph("Course Code & Title:", cell_bold), Paragraph("23CSR306 JAVA PROGRAMMING", cell_norm)],
        [Paragraph("Year / Dept. / Sem / Section:", cell_bold), Paragraph("II / IT / III / A", cell_norm)],
        [Paragraph("Assignment:", cell_bold), Paragraph("II – OOP Mini Project (any one of 35)", cell_norm)],
        [Paragraph("Specification No. & Title:", cell_bold), Paragraph("Specification 2: Library Management System", cell_norm)],
        [Paragraph("GitHub Repository Link:", cell_bold), Paragraph("<font color='#0066cc'>https://github.com/cibi-k/LibraryManagementSystem-JAVA</font>", cell_norm)],
        [Paragraph("Date of Issue:", cell_bold), Paragraph("06-10-2026", cell_norm)],
        [Paragraph("Date of Submission:", cell_bold), Paragraph("", cell_norm)],
    ]

    t_front = Table(front_table_data, colWidths=[180, 350])
    t_front.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.8, colors.HexColor("#333333")),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F0F4F8")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_front)

    story.append(Spacer(1, 14))
    story.append(Paragraph("<b>Marks Details</b>", cell_bold))
    story.append(Spacer(1, 4))

    marks_data = [
        [Paragraph("<b>CO / K Level</b>", cell_bold), Paragraph("<b>Maximum Marks</b>", cell_bold), Paragraph("<b>Marks Obtained</b>", cell_bold)],
        [Paragraph("CO4 / K3", cell_norm), Paragraph("50", cell_norm), Paragraph("", cell_norm)],
        [Paragraph("CO5 / K3", cell_norm), Paragraph("50", cell_norm), Paragraph("", cell_norm)],
        [Paragraph("<b>Total</b>", cell_bold), Paragraph("<b>100</b>", cell_bold), Paragraph("", cell_norm)],
    ]
    t_marks = Table(marks_data, colWidths=[180, 175, 175])
    t_marks.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.8, colors.HexColor("#333333")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor("#E2E8F0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
    ]))
    story.append(t_marks)

    story.append(Spacer(1, 35))
    story.append(Paragraph("<para align='right'><b>Course In-charge Signature: _______________________</b></para>", cell_bold))

    # =============================================================
    # PAGE 2: EVALUATION RUBRICS
    # =============================================================
    story.append(PageBreak())
    story.append(Paragraph("<b>Rubrics for Assignment Evaluation</b>", title_bold))
    story.append(Spacer(1, 8))

    meta_rub = [
        [Paragraph("<b>Assignment Number:</b>", cell_bold), Paragraph("II", cell_norm), Paragraph("<b>Date:</b>", cell_bold), Paragraph("06-10-2026", cell_norm)],
        [Paragraph("<b>Course Code & Title:</b>", cell_bold), Paragraph("23CSR306 Java Programming", cell_norm), Paragraph("<b>Specification:</b>", cell_bold), Paragraph("Spec 2: Library Management System", cell_norm)],
        [Paragraph("<b>Register Number:</b>", cell_bold), Paragraph("717825F112", cell_norm), Paragraph("<b>Student Name:</b>", cell_bold), Paragraph("Cibi K.", cell_norm)]
    ]
    t_mrub = Table(meta_rub, colWidths=[115, 150, 105, 160])
    t_mrub.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#666666")),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F8F9FA")),
        ('BACKGROUND', (2,0), (2,-1), colors.HexColor("#F8F9FA")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_mrub)

    story.append(Spacer(1, 6))
    story.append(Paragraph("<i>Marks for each criterion = Level (1 – 5) × Weightage. Total: 100 (CO4: 50 + CO5: 50).</i>", cell_norm))
    story.append(Spacer(1, 6))

    rubric_cells = [
        [Paragraph("<b>Criterion</b>", cell_bold), Paragraph("<b>CO</b>", cell_bold), Paragraph("<b>Wt</b>", cell_bold),
         Paragraph("<b>Exemplary (5)</b>", cell_bold), Paragraph("<b>Excellent (4)</b>", cell_bold),
         Paragraph("<b>Adequate (3)</b>", cell_bold), Paragraph("<b>Average (2)</b>", cell_bold),
         Paragraph("<b>Inadequate (1)</b>", cell_bold), Paragraph("<b>Max</b>", cell_bold)],

        [Paragraph("Program Correctness & Business Rules", cell_norm), Paragraph("CO4", cell_norm), Paragraph("4", cell_norm),
         Paragraph("All menu options work; every business rule enforced correctly.", cell_norm),
         Paragraph("All options work; minor gaps in one rule.", cell_norm),
         Paragraph("Main flow works; some rules missing.", cell_norm),
         Paragraph("Partially working; several rules not handled.", cell_norm),
         Paragraph("Does not run or most features missing.", cell_norm),
         Paragraph("20", cell_bold)],

        [Paragraph("Input Validation & Exception Handling", cell_norm), Paragraph("CO4", cell_norm), Paragraph("3", cell_norm),
         Paragraph("All inputs validated; custom exceptions; program never crashes.", cell_norm),
         Paragraph("Most inputs validated with try-catch.", cell_norm),
         Paragraph("Basic validation; some invalid inputs not handled.", cell_norm),
         Paragraph("Little validation; crashes on bad input.", cell_norm),
         Paragraph("No validation or exception handling.", cell_norm),
         Paragraph("15", cell_bold)],

        [Paragraph("Menu-driven Interface & Expected Outputs", cell_norm), Paragraph("CO4", cell_norm), Paragraph("3", cell_norm),
         Paragraph("Clear menu; all expected outputs (receipts/status) shown neatly.", cell_norm),
         Paragraph("Clear menu; most expected outputs shown.", cell_norm),
         Paragraph("Menu works; outputs basic or incomplete.", cell_norm),
         Paragraph("Menu unclear; few outputs shown.", cell_norm),
         Paragraph("No proper menu or outputs.", cell_norm),
         Paragraph("15", cell_bold)],

        [Paragraph("OOP Design (Encapsulation, Inheritance, Aggregation, Polymorphism)", cell_norm), Paragraph("CO5", cell_norm), Paragraph("4", cell_norm),
         Paragraph("All four concepts applied meaningfully; all required classes present.", cell_norm),
         Paragraph("Concepts applied well; minor design gaps.", cell_norm),
         Paragraph("Classes present; concepts used in a basic way.", cell_norm),
         Paragraph("Weak design; some required classes missing.", cell_norm),
         Paragraph("No OOP design; mostly procedural.", cell_norm),
         Paragraph("20", cell_bold)],

        [Paragraph("Code Quality & Package Structure", cell_norm), Paragraph("CO5", cell_norm), Paragraph("2", cell_norm),
         Paragraph("Clean packages, naming, indentation and comments.", cell_norm),
         Paragraph("Good structure with few lapses.", cell_norm),
         Paragraph("Acceptable structure; average readability.", cell_norm),
         Paragraph("Poor naming / structure.", cell_norm),
         Paragraph("Single file; unreadable code.", cell_norm),
         Paragraph("10", cell_bold)],

        [Paragraph("GitHub Repository & README", cell_norm), Paragraph("CO5", cell_norm), Paragraph("1", cell_norm),
         Paragraph("Complete code with clear README (problem, run steps, name, roll no.).", cell_norm),
         Paragraph("Complete code; README missing minor details.", cell_norm),
         Paragraph("Code present; README incomplete.", cell_norm),
         Paragraph("Partial code; no README.", cell_norm),
         Paragraph("No repository.", cell_norm),
         Paragraph("5", cell_bold)],

        [Paragraph("Viva / Explanation", cell_norm), Paragraph("CO5", cell_norm), Paragraph("3", cell_norm),
         Paragraph("Explains design, rules and code clearly; answers all questions.", cell_norm),
         Paragraph("Explains well; answers most questions.", cell_norm),
         Paragraph("Explains main logic; answers some questions.", cell_norm),
         Paragraph("Limited explanation of own code.", cell_norm),
         Paragraph("Unable to explain the code.", cell_norm),
         Paragraph("15", cell_bold)]
    ]

    t_rub = Table(rubric_cells, colWidths=[85, 25, 20, 95, 75, 75, 65, 65, 25])
    t_rub.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#666666")),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#D9E1F2")),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ('ALIGN', (1,0), (2,-1), 'CENTER'),
        ('ALIGN', (8,0), (8,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_rub)

    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>CO4 Total (Criteria 1 – 3): 50   |   CO5 Total (Criteria 4 – 7): 50   |   Total Marks: 100</b>", cell_bold))
    story.append(Spacer(1, 14))
    story.append(Paragraph("<b>Signature of the Evaluator with date: _______________________________</b>", cell_bold))

    # =============================================================
    # PAGE 3+: SUBMISSION TEMPLATE & SECTIONS
    # =============================================================
    story.append(PageBreak())

    header_block = [
        [Paragraph("<b>Department of Computer Science and Engineering</b>", cell_norm),
         Paragraph("<para align='right'><b>Reg. No:</b> 717825F112  <b>Name:</b> Cibi K.</para>", cell_norm)]
    ]
    t_hb = Table(header_block, colWidths=[260, 270])
    t_hb.setStyle(TableStyle([
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LINEBELOW', (0,0), (-1,-1), 1, colors.HexColor("#003366")),
    ]))
    story.append(t_hb)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>23CSR306 JAVA PROGRAMMING</b><br/><b>Assignment – II Submission Template</b>", title_bold))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>Specification No. & Title:</b> Specification 2: Library Management System", cell_bold))
    story.append(Spacer(1, 10))

    # 1. Assignment Question
    story.append(Paragraph("1. Assignment Question", section_heading))
    q_text = (
        "<b>Specification 2: Library Management System</b><br/><br/>"
        "<b>Problem Statement:</b> Design and implement a Java console application for a Library Management System "
        "that manages books, members, borrowing, and returns. The system should follow object-oriented principles "
        "and ensure proper tracking of availability.<br/><br/>"
        "<b>Class Requirements:</b> Book, Author, Member, PremiumMember, BorrowTransaction, ReturnTransaction, Library<br/><br/>"
        "<b>Business Rules:</b><br/>"
        "1. Books can only be borrowed if they are available in stock.<br/>"
        "2. When borrowed, stock reduces; when returned, stock updates.<br/>"
        "3. Premium members may borrow more books and for longer duration.<br/>"
        "4. Fines are applied for late returns.<br/>"
        "5. Borrowing and returning transactions must link directly to books.<br/><br/>"
        "<b>Menu Options:</b> Add Book / Add Member / Borrow Book / Return Book / Display Available Books / Exit<br/><br/>"
        "<b>Expected Output:</b><br/>"
        "• Show borrow/return receipt.<br/>"
        "• Display updated stock after each transaction.<br/>"
        "• Show fines (if applicable)."
    )
    t_qbox = Table([[Paragraph(q_text, cell_norm)]], colWidths=[530])
    t_qbox.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#003366")),
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F8F9FA")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(t_qbox)
    story.append(Spacer(1, 14))

    # 2. Java Source Code
    story.append(Paragraph("2. Java Source Code", section_heading))
    story.append(Paragraph("<i>Complete tested Java source code organized package by package: model, exception, service, util, main, and test. Preserves syntax, comments, and package declarations.</i>", cell_norm))
    story.append(Spacer(1, 8))

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

    code_pre_style = ParagraphStyle(
        'CodePreStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7,
        leading=8.5,
        textColor=colors.HexColor("#222222")
    )

    for disp_name, file_path in source_files:
        story.append(Paragraph(f"<b>File: src/com/library/{disp_name}</b>", code_subheading))
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                code_text = f.read()
        else:
            code_text = f"// File not found: {file_path}"

        code_p = Preformatted(code_text, code_pre_style)
        story.append(code_p)
        story.append(Spacer(1, 10))

    # 3. Execution Output Screenshots
    story.append(PageBreak())
    story.append(Paragraph("3. Execution Output Screenshots", section_heading))
    story.append(Paragraph("<i>The following screenshots capture genuine program execution results across all required scenarios from Specification 2.</i>", cell_norm))
    story.append(Spacer(1, 8))

    screenshots = [
        ("screenshots/screen_01_main_menu.png", "Figure 1: Main menu display showing all 6 required options and student information header."),
        ("screenshots/screen_02_add_book_and_member.png", "Figure 2: Successfully adding new Book (BK-105: Spring in Action) and registering Regular and Premium members."),
        ("screenshots/screen_03_borrow_receipt.png", "Figure 3: Official borrow receipt for Regular Member MEM-001 showing 14-day loan and stock decrement (2 -> 1)."),
        ("screenshots/screen_04_premium_and_stock_validation.png", "Figure 4: Premium Member borrowing privilege (30-day loan) and subsequent borrow rejection due to zero stock (0/1)."),
        ("screenshots/screen_05_return_ontime_receipt.png", "Figure 5: On-time return receipt for TXN-1001 with stock restored (1 -> 2) and Rs. 0.00 fine."),
        ("screenshots/screen_06_return_overdue_fine.png", "Figure 6: Return receipt showing overdue fine calculation (10 days @ Rs.5/day = Rs.50.00) and duplicate return rejection."),
        ("screenshots/screen_07_display_available_books.png", "Figure 7: Display Available Books table and validation handling of invalid menu inputs without crashing."),
    ]

    base_dir = r"C:\Users\kcibi\.gemini\antigravity\scratch\LibraryManagementSystem-JAVA"
    from PIL import Image as PILImage
    for img_rel, cap in screenshots:
        img_abs = os.path.join(base_dir, img_rel)
        if os.path.exists(img_abs):
            with PILImage.open(img_abs) as pimg:
                w, h = pimg.size
            disp_w = 490
            disp_h = int(disp_w * h / w)
            story.append(Image(img_abs, width=disp_w, height=disp_h))
            story.append(Paragraph(cap, caption_style))
            story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Eclipse Console Capture Instructions:</b><br/>"
                           "To capture directly from Eclipse IDE:<br/>"
                           "1. In Eclipse, select <b>File -> Import... -> General -> Existing Projects into Workspace</b>.<br/>"
                           "2. Choose directory <code>C:\\Users\\kcibi\\.gemini\\antigravity\\scratch\\LibraryManagementSystem-JAVA</code> and click <b>Finish</b>.<br/>"
                           "3. Right-click <code>Main.java</code> -> <b>Run As -> Java Application</b>.<br/>"
                           "4. Enter choices 1 to 6 to reproduce the scenarios and capture using Windows Snipping Tool (Win+Shift+S).", cell_norm))
    story.append(Spacer(1, 14))

    # 4. GitHub Repository Link
    story.append(PageBreak())
    story.append(Paragraph("4. GitHub Repository Link", section_heading))

    gh_table_data = [
        [Paragraph("<b>GitHub Repository URL:</b>", cell_bold), Paragraph("<font color='#0066cc'><b>https://github.com/cibi-k/LibraryManagementSystem-JAVA</b></font>", cell_norm)],
        [Paragraph("<b>Repository Name:</b>", cell_bold), Paragraph("LibraryManagementSystem-JAVA", cell_norm)],
        [Paragraph("<b>Student Author:</b>", cell_bold), Paragraph("Cibi K. (Register No: 717825F112)", cell_norm)],
        [Paragraph("<b>Branch:</b>", cell_bold), Paragraph("main", cell_norm)],
        [Paragraph("<b>README Documentation:</b>", cell_bold), Paragraph("Contains full problem statement, all 5 business rules, complete OOP architecture analysis, Eclipse import steps, CLI commands, verified 17-scenario test matrix, and loan/fine policies.", cell_norm)]
    ]
    t_gh = Table(gh_table_data, colWidths=[160, 370])
    t_gh.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.8, colors.HexColor("#003366")),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor("#F0F4F8")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_gh)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report PDF built successfully at: {pdf_path}")

if __name__ == "__main__":
    build_pdf_report()
