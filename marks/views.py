from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Student, MarkField, Mark
from .forms import StudentForm, MarkFieldForm
import openpyxl
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors


@login_required
def dashboard(request):
    students = Student.objects.filter(teacher=request.user)
    fields = MarkField.objects.filter(teacher=request.user)

    # 📝 Handle form submissions
    if request.method == "POST":
        # ➕ Add Student
        if "add_student" in request.POST:
            sform = StudentForm(request.POST)
            if sform.is_valid():
                stu = sform.save(commit=False)
                stu.teacher = request.user
                stu.save()
            return redirect("dashboard")

        # ➕ Add Field
        elif "add_field" in request.POST:
            fform = MarkFieldForm(request.POST)
            if fform.is_valid():
                fld = fform.save(commit=False)
                fld.teacher = request.user
                fld.save()
            return redirect("dashboard")

        # 💾 Save Marks (create or update)
        elif "save_marks" in request.POST:
            for s in students:
                for f in fields:
                    field_name = f"mark_{s.id}_{f.id}"
                    score = request.POST.get(field_name)
                    if score is not None:
                        try:
                            score_val = int(score)
                        except ValueError:
                            score_val = 0
                        mark, _ = Mark.objects.get_or_create(student=s, field=f)
                        mark.score = score_val
                        mark.save()
            return redirect("dashboard")

    # 📊 Build student data for rendering
    students_data, totals = [], []
    for s in students:
        row_marks, total = [], 0
        for f in fields:
            m, _ = Mark.objects.get_or_create(student=s, field=f, defaults={"score": 0})
            row_marks.append(m)
            total += m.score
        students_data.append({"student": s, "marks": row_marks, "overall": total})
        totals.append(total)

    avg_score = round(sum(totals) / len(totals), 2) if totals else 0

    return render(request, "marks/dashboard.html", {
        "students": students,
        "fields": fields,
        "students_data": students_data,
        "avg_score": avg_score,
        "student_form": StudentForm(),
        "field_form": MarkFieldForm(),
    })


@login_required
def export_excel(request):
    students = Student.objects.filter(teacher=request.user)
    fields = MarkField.objects.filter(teacher=request.user)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Marks"
    ws.append(["Student"] + [f.name for f in fields] + ["Overall"])

    for s in students:
        row, total = [s.name], 0
        for f in fields:
            m = Mark.objects.filter(student=s, field=f).first()
            score = m.score if m else 0
            row.append(score)
            total += score
        row.append(total)
        ws.append(row)

    resp = HttpResponse(content_type="application/vnd.ms-excel")
    resp["Content-Disposition"] = 'attachment; filename="marks.xlsx"'
    wb.save(resp)
    return resp


@login_required
def export_pdf(request):
    students = Student.objects.filter(teacher=request.user)
    fields = MarkField.objects.filter(teacher=request.user)

    data = [["Student"] + [f.name for f in fields] + ["Overall"]]
    for s in students:
        row, total = [s.name], 0
        for f in fields:
            m = Mark.objects.filter(student=s, field=f).first()
            score = m.score if m else 0
            row.append(score)
            total += score
        row.append(total)
        data.append(row)

    resp = HttpResponse(content_type="application/pdf")
    resp["Content-Disposition"] = 'attachment; filename="marks.pdf"'

    doc = SimpleDocTemplate(resp)
    table = Table(data)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.darkgray),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
    ]))
    doc.build([table])
    return resp


