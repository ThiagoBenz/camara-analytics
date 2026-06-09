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

  getEixosDeputados() {
    return this.http.get(`${this.apiUrl}/eixos-deputados`);
  }

  getEixosResumo() {
    return this.http.get(`${this.apiUrl}/eixos-resumo`);
  }

  getEscolaridadeResumo() {
    return this.http.get(`${this.apiUrl}/escolaridade-resumo`);
  }

  getEscolaridadeDeputados(grupo?: string) {
    const url = grupo 
      ? `${this.apiUrl}/escolaridade-deputados?grupo=${encodeURIComponent(grupo)}`
      : `${this.apiUrl}/escolaridade-deputados`;
    return this.http.get(url);
  }

  getNuvemPalavras(eixo: string) {
    return this.http.get(
      `${this.apiUrl}/nuvem-palavras/${encodeURIComponent(eixo)}`
    );
  }

  getFornecedoresDeputado(nome: string) {
    return this.http.get(
      `${this.apiUrl}/correlacao-fornecedor-deputado/${encodeURIComponent(nome)}`
    );
  }

}