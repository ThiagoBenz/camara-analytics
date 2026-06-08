import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ApiService } from '../../services/api.service';

type EixoResumo = {
  eixo: string;
  total_deputados: number;
  score_total: number;
  gasto_total: number;
};

type DeputadoEixo = {
  id_deputado: number;
  nome: string;
  partido: string;
  uf: string;
  eixo: string;
  score: number;
  total_gasto: number;
};

type PalavraNuvem = {
  word: string;
  count: number;
};

@Component({
  selector: 'app-eixos-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './eixos-dashboard.component.html',
  styleUrl: './eixos-dashboard.component.css'
})
export class EixosDashboardComponent implements OnInit {
  readonly eixosDisponiveis = [
    'Economia',
    'Saúde',
    'Educação',
    'Segurança Pública',
    'Meio Ambiente',
    'Tributação',
    'Direitos Sociais'
  ];

  resumoEixos: EixoResumo[] = [];
  deputadosEixo: DeputadoEixo[] = [];
  palavras: PalavraNuvem[] = [];

  eixoSelecionado = this.eixosDisponiveis[0];
  carregando = false;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.carregarDados();
  }

  carregarDados(): void {
    this.carregando = true;

    this.apiService.getEixosResumo().subscribe({
      next: (data: any) => {
        this.resumoEixos = Array.isArray(data) ? data : [];
      },
      error: () => {
        this.resumoEixos = [];
      }
    });

    this.apiService.getEixosDeputados().subscribe({
      next: (data: any) => {
        this.deputadosEixo = Array.isArray(data) ? data : [];
        this.carregarNuvem();
      },
      error: () => {
        this.deputadosEixo = [];
        this.palavras = [];
        this.carregando = false;
      }
    });
  }

  alterarEixo(eixo: string): void {
    this.eixoSelecionado = eixo;
    this.carregarNuvem();
  }

  carregarNuvem(): void {
    this.apiService.getNuvemPalavras(this.eixoSelecionado).subscribe({
      next: (data: any) => {
        this.palavras = Array.isArray(data) ? data : [];
        this.carregando = false;
      },
      error: () => {
        this.palavras = [];
        this.carregando = false;
      }
    });
  }

  get deputadosFiltrados(): DeputadoEixo[] {
    return this.deputadosEixo.filter((item) => item.eixo === this.eixoSelecionado);
  }

  get totalDeputados(): number {
    return this.resumoEixos.reduce((total, item) => total + (item.total_deputados || 0), 0);
  }

  tamanhoPalavra(count: number): number {
    return Math.min(34, 14 + count * 2);
  }
}