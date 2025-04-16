Sub Stonereport()
    Dim arrObjects, strObject, SELOBJS, NAME, COUNT, MOBJ, WT
    Dim Total, TotWt, WeightGrade, PiecesGrade, FinalGrade
    Dim A_total, StoneArea, RemainingArea
    Total = 0
    TotWt = 0
    A_total = 100 ' Assume total area of the jewelry piece (this value should be defined based on your design)

    ' Initialize RemainingArea as the total area initially
    RemainingArea = A_total

    ' Report Header
    C = "STONE SIZE REPORT:124 " & vbCrLf & vbCrLf

    ' Loop through stone sizes
    For NAME = 0.5 To 9 Step 0.1
        NAME = FormatNumber(NAME, 1)
        Rhino.UnselectAllObjects

        ' Select objects by name
        If NAME <> vbNull Then
            arrObjects = Rhino.ObjectsByName(NAME, vbTrue)
        End If
        SELOBJS = Rhino.SelectedObjects

        If Not IsNull(SELOBJS) And IsArray(SELOBJS) Then
            COUNT = 0
            For Each MOBJ In SELOBJS
                COUNT = COUNT + 1
                Total = Total + 1
            Next

            ' Assign weight based on size
            If NAME >= 0.5 And NAME <= 0.9 Then
                WT = 0.0012
            ElseIf NAME >= 1.0 And NAME <= 1.2 Then
                WT = 0.002
            ElseIf NAME = 1.3 Then
                WT = 0.003
            ElseIf NAME = 1.4 Then
                WT = 0.004
            ElseIf NAME >= 1.5 And NAME <= 1.6 Then
                WT = 0.006
            Else
                WT = 0
            End If

            ' Calculate stone area (assuming stones are circular)
            StoneArea = 3.1416 * (NAME / 2) ^ 2 * COUNT

            ' Update Remaining Area
            RemainingArea = RemainingArea - StoneArea

            ' Update report and totals
            S = NAME & " MM= " & COUNT & " NOS" & " (WT= " & COUNT * WT & " GMS)" & _
                " (Area = " & StoneArea & " sq.mm)"
            C = C & S & vbCrLf
            TotWt = TotWt + COUNT * WT
        End If
    Next

    ' Determine grades
    WeightGrade = GetGrade(TotWt, "weight")
    PiecesGrade = GetGrade(Total, "pieces")
    FinalGrade = Round((WeightGrade + PiecesGrade) / 2, 1)

    ' Add final summary
    TOT = C & vbCrLf & "TOTAL = " & Total & " NOS" & vbCrLf & _
          "TOTAL WT = " & TotWt & " GMS" & vbCrLf & _
          "FINAL GRADE = " & FinalGrade & vbCrLf & _
          "REMAINING AREA = " & RemainingArea & " sq.mm"

    MsgBox TOT, 0, ("STONE SIZE REPORT")
    Rhino.Print "TOTAL = " & Total & " NOS"
    Rhino.Print "TOTAL WT = " & TotWt & " GMS"
    Rhino.Print "FINAL GRADE = " & FinalGrade
    Rhino.Print "REMAINING AREA = " & RemainingArea & " sq.mm"
End Sub

Function GetGrade(Value, Type)
    Dim GradeRanges, RangeKey, RangeParts
    Set GradeRanges = CreateObject("Scripting.Dictionary")

    ' Define grade ranges based on type
    If Type = "weight" Then
        GradeRanges.Add "0-1.99", 0.2
        GradeRanges.Add "2-3.99", 0.4
        GradeRanges.Add "4-5.99", 0.6
        ' Add additional weight ranges
    ElseIf Type = "pieces" Then
        GradeRanges.Add "0-10", 0.1
        GradeRanges.Add "10-20", 0.25
        GradeRanges.Add "20-30", 0.4
        ' Add additional pieces ranges
    End If

    ' Find grade range
    For Each RangeKey In GradeRanges.Keys
        RangeParts = Split(RangeKey, "-")
        If Value >= CDbl(RangeParts(0)) And Value <= CDbl(RangeParts(1)) Then
            GetGrade = GradeRanges.Item(RangeKey)
            Exit Function
        End If
    Next

    ' Default grade if not found
    GetGrade = 0
End Function
