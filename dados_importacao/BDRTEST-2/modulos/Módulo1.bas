Attribute VB_Name = "Módulo1"
Option Compare Database
Option Explicit

Sub ImportarProposicoes2020a2025()
    Dim arq(5) As String
    Dim qtdImp As Long
    Dim qtdErr As Long
    Dim totalImp As Long
    Dim totalErr As Long
    Dim i As Integer

    arq(0) = "C:\Users\shiro\Desktop\BDRTEST\proposicoes-2020.csv"
    arq(1) = "C:\Users\shiro\Desktop\BDRTEST\proposicoes-2021.csv"
    arq(2) = "C:\Users\shiro\Desktop\BDRTEST\proposicoes-2022.csv"
    arq(3) = "C:\Users\shiro\Desktop\BDRTEST\proposicoes-2023.csv"
    arq(4) = "C:\Users\shiro\Desktop\BDRTEST\proposicoes-2024.csv"
    arq(5) = "C:\Users\shiro\Desktop\BDRTEST\proposicoes-2025.csv"

    totalImp = 0
    totalErr = 0

    For i = 0 To 5
        Call ImportarProposicoesCSV(arq(i), qtdImp, qtdErr)
        totalImp = totalImp + qtdImp
        totalErr = totalErr + qtdErr
    Next i

    MsgBox "TOTAL Importados: " & totalImp & vbCrLf & "TOTAL Erros: " & totalErr
End Sub

' Parser CSV que respeita aspas e quebras de linha dentro de campos
Function ParseCSVLine(linha As String, sep As String) As String()
    Dim resultado() As String
    Dim campos As New Collection
    Dim i As Long
    Dim c As String
    Dim campo As String
    Dim dentroAspas As Boolean

    campo = ""
    dentroAspas = False

    For i = 1 To Len(linha)
        c = Mid(linha, i, 1)
        If c = Chr(34) Then
            dentroAspas = Not dentroAspas
        ElseIf c = sep And Not dentroAspas Then
            campos.Add campo
            campo = ""
        Else
            campo = campo & c
        End If
    Next i
    campos.Add campo

    ReDim resultado(campos.Count - 1)
    Dim j As Integer
    For j = 1 To campos.Count
        resultado(j - 1) = campos(j)
    Next j
    ParseCSVLine = resultado
End Function

' Junta linhas quebradas dentro de campos com aspas
Function MontarRegistros(conteudo As String) As Collection
    Dim resultado As New Collection
    Dim linhas() As String
    Dim registro As String
    Dim linha As String
    Dim i As Long
    Dim contAspas As Long
    Dim j As Long

    linhas = Split(conteudo, vbLf)
    registro = ""

    For i = 0 To UBound(linhas)
        linha = linhas(i)
        linha = Replace(linha, Chr(13), "")

        If registro = "" Then
            registro = linha
        Else
            registro = registro & " " & linha
        End If

        contAspas = 0
        For j = 1 To Len(registro)
            If Mid(registro, j, 1) = Chr(34) Then contAspas = contAspas + 1
        Next j

        If contAspas Mod 2 = 0 Then
            resultado.Add registro
            registro = ""
        End If
    Next i

    If registro <> "" Then resultado.Add registro
    Set MontarRegistros = resultado
End Function

Sub ImportarProposicoesCSV(caminho As String, qtdImp As Long, qtdErr As Long)
    Dim oStream As Object
    Dim db As Object
    Dim rs As Object
    Dim col() As String
    Dim conteudo As String
    Dim registros As Collection
    Dim registro As Variant
    Dim i As Long

    qtdImp = 0
    qtdErr = 0

    If Dir(caminho) = "" Then
        MsgBox "Nao encontrado: " & caminho
        Exit Sub
    End If

    Set oStream = CreateObject("ADODB.Stream")
    oStream.Charset = "UTF-8"
    oStream.Open
    oStream.LoadFromFile caminho
    conteudo = oStream.ReadText
    oStream.Close
    Set oStream = Nothing

    Set registros = MontarRegistros(conteudo)

    Set db = CurrentDb()
    Set rs = db.OpenRecordset("Proposicoes", 1)

    i = 0
    For Each registro In registros
        i = i + 1
        If i = 1 Then GoTo Prox

        col = ParseCSVLine(CStr(registro), ";")

        If UBound(col) < 15 Then GoTo Prox
        If Trim(col(0)) = "" Then GoTo Prox
        If Not IsNumeric(Trim(col(0))) Then GoTo Prox

        On Error Resume Next
        rs.AddNew
        rs!id_proposicao = CLng(Trim(col(0)))
        rs!sigla_tipo_proposicao = Left(Trim(col(2)), 10)
        If Trim(col(3)) <> "" Then rs!numero_proposicao = CLng(Trim(col(3)))
        If Trim(col(4)) <> "" Then rs!ano_proposicao = CInt(Trim(col(4)))
        If Trim(col(5)) <> "" Then rs!cod_tipo_proposicao = CLng(Trim(col(5)))
        rs!descricao_tipo_proposicao = Trim(col(6))
        rs!ementa = Trim(col(7))
        rs!ementa_detalhada = Trim(col(8))
        rs!keywords = Trim(col(9))
        If Trim(col(10)) <> "" Then rs!data_apresentacao = CDate(Left(Trim(col(10)), 10))
        rs!url_inteiro_teor = Trim(col(15))
        If Trim(col(17)) <> "" Then rs!ultimo_status_data_hora = CDate(Left(Trim(col(17)), 10))
        rs!ultimo_status_regime = Trim(col(23))
        rs!ultimo_status_descricao_tramitacao = Trim(col(24))
        rs!ultimo_status_descricao_situacao = Trim(col(26))
        If Trim(col(27)) <> "" Then rs!ultimo_status_id_situacao = CLng(Trim(col(27)))
        rs!ultimo_status_apreciacao = Trim(col(29))
        rs.Update
        If Err.Number <> 0 Then
            qtdErr = qtdErr + 1
            Err.Clear
        Else
            qtdImp = qtdImp + 1
        End If
        On Error GoTo 0
Prox:
    Next registro

    rs.Close
    Set rs = Nothing
    Set db = Nothing
End Sub
