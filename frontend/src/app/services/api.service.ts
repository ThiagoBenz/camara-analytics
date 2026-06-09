  import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  getRankingGastos() {
    return this.http.get(`${this.apiUrl}/ranking-gastos`);
  }
  
  getDeputados() {
  return this.http.get('http://127.0.0.1:8000/deputados');
  }

  getGastosDeputado(nome: string) {
    return this.http.get(
      `http://127.0.0.1:8000/deputado-gastos/${encodeURIComponent(nome)}`
    )
  }

  getFornecedoresDeputado(nome: string) {
    return this.http.get(
      `${this.apiUrl}/correlacao-fornecedor-deputado/${encodeURIComponent(nome)}`
    )
  }

  getDashboard() {
    return this.http.get(
      `${this.apiUrl}/dashboard`
    )
  }

  getDashboardDestaques() {

    return this.http.get(
      `${this.apiUrl}/dashboard-destaques`
  )

  }

  getDashboardFornecedores() {

  return this.http.get(
    `${this.apiUrl}/dashboard-fornecedores`
  );

}

}