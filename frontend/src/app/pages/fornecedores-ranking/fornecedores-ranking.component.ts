import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

type FornecedorRanking = {
  cnpj_cpf: string;
  nome_fornecedor: string;
  total_recebido: number;
  qtd_despesas: number;
};

@Component({
  selector: 'app-fornecedores-ranking',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './fornecedores-ranking.component.html',
  styleUrl: './fornecedores-ranking.component.css'
})
export class FornecedoresRankingComponent implements OnInit {
  fornecedores: FornecedorRanking[] = [];
  termoBusca: string = '';
  termoBuscaPesquisado: string = '';
  limit: number = 20;
  paginaAtual: number = 1;
  carregando: boolean = false;
  possuiMais: boolean = true;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.carregarRanking();
  }

  carregarRanking(): void {
    this.carregando = true;
    const offset = (this.paginaAtual - 1) * this.limit;
    
    this.apiService.getFornecedoresRanking(this.termoBuscaPesquisado, this.limit, offset).subscribe({
      next: (data: any) => {
        this.fornecedores = Array.isArray(data) ? data : [];
        this.possuiMais = this.fornecedores.length === this.limit;
        this.carregando = false;
      },
      error: () => {
        this.fornecedores = [];
        this.possuiMais = false;
        this.carregando = false;
      }
    });
  }

  buscar(): void {
    this.termoBuscaPesquisado = this.termoBusca.trim();
    this.paginaAtual = 1;
    this.carregarRanking();
  }

  limparBusca(): void {
    this.termoBusca = '';
    this.termoBuscaPesquisado = '';
    this.paginaAtual = 1;
    this.carregarRanking();
  }

  paginaAnterior(): void {
    if (this.paginaAtual > 1) {
      this.paginaAtual--;
      this.carregarRanking();
    }
  }

  proximaPagina(): void {
    if (this.possuiMais) {
      this.paginaAtual++;
      this.carregarRanking();
    }
  }

  get rankingInicial(): number {
    return (this.paginaAtual - 1) * this.limit + 1;
  }
}
