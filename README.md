# Library Management System (Java OOP Mini-Project)

**Course:** 23CSR306 — Java Programming  
**Assignment:** Assignment II — OOP Mini Project  
**Selected Specification:** Specification 2 — Library Management System  
**Academic Year:** 2026–2027 | **Semester:** III | **Year:** II | **Dept:** IT | **Section:** A  
**Student Name:** Cibi K.  
**Register Number:** 717825F112  
**Institution:** Karpagam College of Engineering (Autonomous), Coimbatore  
**GitHub Repository:** [https://github.com/cibi-k/LibraryManagementSystem-JAVA](https://github.com/cibi-k/LibraryManagementSystem-JAVA)  
**Date of Issue:** 06-10-2026  

---

## 1. Problem Statement

> **"Design and implement a Java console application for a Library Management System that manages books, members, borrowing, and returns. The system should follow object-oriented principles and ensure proper tracking of availability."**

---

## 2. Business Rules (Mandatory Specification Requirements)

1. **Stock Verification:** Books can only be borrowed if they are available in stock (`availableCopies > 0`). If a book has 0 copies remaining, borrow requests are immediately rejected.
2. **Dynamic Stock Tracking:** When a book is borrowed, its available stock decreases immediately by 1; when a book is returned, its stock is automatically incremented.
3. **Privilege-based Membership Quotas:** Premium members may borrow more books and for a longer duration compared to regular members.
4. **Late Return Fine Enforcement:** Overdue fines are automatically assessed when a book is returned after its scheduled due date.
5. **Direct Relational Linkage:** Borrowing and returning transactions must link directly to the actual book and member entities involved.

---

## 3. Membership & Fine Policy Specifications

To fulfill Business Rules 3 and 4 with consistent business logic, the following parameters are enforced across the application and automated tests:

| Parameter | Regular Member | Premium Member (`Gold` / `Platinum` / `VIP`) | Rationale / Rule Reference |
| :--- | :--- | :--- | :--- |
| **Max Concurrent Books Allowed** | **3 books** | **6 books** | Premium members borrow more books (Rule 3) |
| **Standard Borrow Duration** | **14 days** | **30 days** | Premium members borrow for longer duration (Rule 3) |
| **Daily Overdue Fine Rate** | **₹ 5.00 / day** | **₹ 2.00 / day** | Discounted fine rate for premium tier |
| **Eligibility Verification** | Quota check (< 3) | Quota check (< 6) | Enforced polymorphically via `canBorrow()` |

---

## 4. Object-Oriented Programming (OOP) Architecture

The application is structured to showcase all four fundamental OOP principles:

### A. Encapsulation
- All data fields across model and service classes (`bookId`, `title`, `availableCopies`, `memberId`, `currentlyBorrowedCount`, `borrowDate`, `dueDate`, `fineAmount`) are declared `private`.
- Controlled access is provided via public getters and validated mutators (setters).
- Business invariants (e.g., negative stock, null names, out-of-range dates) are strictly defended inside setter methods by throwing `IllegalArgumentException`.

### B. Inheritance
- `PremiumMember` extends the base class `Member`.
- The child class inherits fundamental identity fields (`memberId`, `name`, `phone`, `currentlyBorrowedCount`) while introducing premium attributes (`membershipTier`).
- Reduces boilerplate and models the "is-a" domain relationship (`PremiumMember` is-a `Member`).

### C. Polymorphism
- Dynamic method dispatch is applied across member privileges:
  - `getMaxBooksAllowed()`: Overridden in `PremiumMember` to return `6` instead of `3`.
  - `getBorrowDurationDays()`: Overridden in `PremiumMember` to return `30` instead of `14`.
  - `getDailyFineRate()`: Overridden in `PremiumMember` to return `2.00` instead of `5.00`.
  - `getMembershipType()`: Overridden to reflect the tier (e.g. `Premium Member [Platinum]`).
- When a loan or return is processed, the system invokes these methods on the `Member` reference, dynamically applying the appropriate quota, loan duration, and fine rate without cumbersome `if-else` type inspections.

### D. Aggregation and Composition
- **Book and Author (Aggregation):** A `Book` maintains a direct reference to an `Author` object (`Book` HAS-A `Author`). Authors exist independently of individual book titles.
- **Transactions and Entities (Association/Linkage):** `BorrowTransaction` and `ReturnTransaction` retain direct object references to `Book` and `Member` instances, satisfying Business Rule 5.
- **Library Catalog (Composition):** The `Library` orchestrator manages books, members, and transactions in memory using robust collections (`Map` and `List`).

---

## 5. Required Classes and Package Structure

```
LibraryManagementSystem-JAVA/
├── .classpath                          # Eclipse classpath descriptor (JavaSE-17)
├── .gitignore                          # Standard git ignore for compiled classes and IDE caches
├── .project                            # Eclipse project descriptor
├── README.md                           # Comprehensive documentation and project guide
├── bin/                                # Compiled .class bytecode (generated on build)
├── docs/                               # Execution logs and report sources
│   ├── execution_summary.md
│   ├── terminal_execution_output.txt
│   └── render_screenshots.py
├── screenshots/                        # Captured terminal output screenshots
│   ├── screen_01_main_menu.png
│   ├── screen_02_add_book_and_member.png
│   ├── screen_03_borrow_receipt.png
│   ├── screen_04_premium_and_stock_validation.png
│   ├── screen_05_return_ontime_receipt.png
│   ├── screen_06_return_overdue_fine.png
│   └── screen_07_display_available_books.png
└── src/
    └── com/
        └── library/
            ├── exception/              # Custom domain-specific checked exceptions
            │   ├── BookNotFoundException.java
            │   ├── BorrowLimitExceededException.java
            │   ├── DuplicateEntityException.java
            │   ├── InsufficientStockException.java
            │   ├── InvalidTransactionException.java
            │   ├── LibraryException.java
            │   └── MemberNotFoundException.java
            ├── main/
            │   └── Main.java           # Menu-driven console interface with input validation
            ├── model/                  # Core domain entities
            │   ├── Author.java         # Required Author class
            │   ├── Book.java           # Required Book class (stock tracking)
            │   ├── BorrowTransaction.java # Required BorrowTransaction class
            │   ├── Member.java         # Required base Member class
            │   ├── PremiumMember.java  # Required subclass PremiumMember
            │   └── ReturnTransaction.java # Required ReturnTransaction class
            ├── service/
            │   └── Library.java        # Required Library service orchestrator
            ├── test/
            │   └── LibrarySystemTest.java # Automated verification suite (17 scenarios)
            └── util/
                └── ValidationUtil.java # Scanner input validation & date handling helpers
```

---

## 6. Prerequisites

- **Java Development Kit (JDK):** JDK 17 or higher (tested on OpenJDK / Oracle JDK 17+ and JDK 25 LTS).
- **IDE (Recommended):** Eclipse IDE for Java Developers (2022-09 or newer).
- **Terminal:** PowerShell, Command Prompt, or bash for CLI compilation and execution.

---

## 7. How to Import and Run in Eclipse IDE

1. **Open Eclipse IDE.**
2. Go to **File -> Import...**
3. Select **General -> Existing Projects into Workspace**, then click **Next**.
4. Click **Browse...** next to *Select root directory* and navigate to:
   ```
   C:\Users\kcibi\.gemini\antigravity\scratch\LibraryManagementSystem-JAVA
   ```
5. Ensure `LibraryManagementSystem-JAVA` is checked in the Projects list and click **Finish**.
6. In the **Package Explorer**, expand:
   `src -> com.library.main -> Main.java`
7. Right-click `Main.java`, choose **Run As -> Java Application**.
8. The interactive console menu will appear in Eclipse's **Console** view at the bottom.
9. To run the automated verification suite:
   Right-click `src/com/library/test/LibrarySystemTest.java` -> **Run As -> Java Application**.

---

## 8. How to Compile and Run via Command Line

Open PowerShell or Command Prompt inside the project directory:

```powershell
# Navigate to the repository root
cd C:\Users\kcibi\.gemini\antigravity\scratch\LibraryManagementSystem-JAVA

# Compile all source files into bin directory
cmd.exe /c "javac -d bin src\com\library\model\*.java src\com\library\exception\*.java src\com\library\service\*.java src\com\library\util\*.java src\com\library\main\*.java src\com\library\test\*.java"

# Run the interactive menu-driven application
java -cp bin com.library.main.Main

# Run the 17-scenario automated test suite
java -cp bin com.library.test.LibrarySystemTest
```

---

## 9. Test Verification Matrix (17 Test Scenarios)

All 17 required scenarios were executed and verified against `LibrarySystemTest.java`:

| # | Scenario / Test Case | Expected Behavior | Execution Result | Status |
| :---: | :--- | :--- | :--- | :---: |
| **01** | App Initialization | Library initializes cleanly with empty/seeded state | Catalog & registry online | **PASS** |
| **02** | Add Valid Book | Book stored with ISBN, Author, and stock | Book `BK-201` registered | **PASS** |
| **03** | Add Regular Member | Created with 3 books limit, 14 days loan, ₹5/day fine | Member `MEM-101` registered | **PASS** |
| **04** | Add Premium Member | Created with 6 books limit, 30 days loan, ₹2/day fine | Member `PREM-101` registered | **PASS** |
| **05** | Successful Borrow | Borrow approved, transaction created, receipt generated | Borrow receipt generated | **PASS** |
| **06** | Stock Decrement | Available stock decrements immediately on borrow | Available stock: 2 -> 1 | **PASS** |
| **07** | Out of Stock Check | Borrow rejected when available stock is 0 | Throws `InsufficientStockException` | **PASS** |
| **08** | Invalid Member ID | Borrow rejected when member is not found | Throws `MemberNotFoundException` | **PASS** |
| **09** | Regular Quota Exceeded | Borrowing > 3 books rejected for regular member | Throws `BorrowLimitExceededException` | **PASS** |
| **10** | Premium Privileges | Allows up to 6 books and grants 30 days due date | 4th borrow approved; due in 30d | **PASS** |
| **11** | On-Time Return | Return approved, receipt emitted, ₹0.00 fine | Due date honored; fine is ₹0.00 | **PASS** |
| **12** | Stock Increment | Available stock increments back after return | Stock restored: 1 -> 2 | **PASS** |
| **13** | Overdue Fine Calculation | Computes overdue days × daily rate | 5 days late × ₹5 = ₹25.00 | **PASS** |
| **14** | Unborrowed/Duplicate Return| Prevents returning unborrowed/already returned book | Throws `InvalidTransactionException` | **PASS** |
| **15** | Input & Duplicate ID Protection | Rejects duplicate IDs and invalid input gracefully | Throws `DuplicateEntityException` | **PASS** |
| **16** | Display Available Books | Filters catalog to show books where stock > 0 | Correct filtered list returned | **PASS** |
| **17** | State Integrity & Clean Exit | Validates stock bounds & member counts across lifecycle | Zero state leaks; clean exit | **PASS** |

---

## 10. Sample Output Receipts

### A. Official Borrow Receipt
```
============================================================
                 OFFICIAL BORROW RECEIPT                    
============================================================
 Transaction ID     : TXN-1001
 Borrow Date        : 10-10-2026
 Due Date           : 24-10-2026 (14 days allowed)
------------------------------------------------------------
 MEMBER DETAILS:
 Member ID          : MEM-001
 Member Name        : Cibi K.
 Membership Tier    : Regular Member
 Active Borrows     : 1 / 3 books
------------------------------------------------------------
 BOOK DETAILS:
 Book ID            : BK-101
 Title              : Effective Java
 Author             : Joshua Bloch
 ISBN               : 978-0134685991
 Updated Stock      : 1 available (Total: 2)
============================================================
```

### B. Official Return Receipt (With Overdue Fine)
```
============================================================
                 OFFICIAL RETURN RECEIPT                    
============================================================
 Return Txn ID      : RET-5002
 Original Borrow Txn: TXN-1003
 Return Date        : 25-10-2026
 Scheduled Due Date : 15-10-2026
------------------------------------------------------------
 MEMBER DETAILS:
 Member ID          : MEM-002
 Member Name        : Dinesh Kumar
 Membership Tier    : Regular Member
 Remaining Borrows  : 0 / 3 books
------------------------------------------------------------
 BOOK DETAILS:
 Book ID            : BK-102
 Title              : Clean Code: A Handbook of Agile Craftsmanship
 Author             : Robert C. Martin
 Updated Stock      : 3 available (Total: 3)
------------------------------------------------------------
 FINE ASSESSMENT:
 Overdue Duration   : 10 day(s) late
 Daily Fine Rate    : Rs. 5.00/day
 Total Fine Due     : Rs. 50.00 [APPLIED]
============================================================
```

---

## 11. Viva Preparation Quick Reference

- **Encapsulation:** Used in all entities. Attributes like `availableCopies` in `Book` cannot be modified directly; changes go through `borrowCopy()` and `returnCopy()` which enforce stock constraints.
- **Inheritance:** `PremiumMember extends Member`. Reuses common attributes (`name`, `phone`) while extending functionality with membership tiers.
- **Polymorphism:** Method overriding in `Member` vs `PremiumMember`. For example, `member.getMaxBooksAllowed()` returns 3 for regular members and 6 for premium members. The library code calls `member.canBorrow()` without needing to check `instanceof`.
- **Aggregation:** `Book` has an `Author`. If a `Book` is removed, the `Author` can still exist independently.
- **Exception Handling:** Custom checked exceptions (`InsufficientStockException`, `BorrowLimitExceededException`, etc.) provide descriptive domain error messages without crashing the console loop.
