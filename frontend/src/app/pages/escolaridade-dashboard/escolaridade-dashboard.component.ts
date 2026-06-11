import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';

type EscolaridadeResumo = {
  grupo_escolaridade: string;
  total_deputados: number;
  gasto_total: number;
  gasto_medio: number;
};

type DeputadoEscolaridade = {
  id_deputado: number;
  nome: string;
  partido: string;
  uf: string;
  escolaridade_original: string;
  escolaridade_limpa: string;
  grupo_escolaridade: string;
  total_gasto: number;
};

@Component({
  selector: 'app-escolaridade-dashboard',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './escolaridade-dashboard.component.html',
  styleUrl: './escolaridade-dashboard.component.css'
})
export class EscolaridadeDashboardComponent implements OnInit {
  resumo: EscolaridadeResumo[] = [];
  deputados: DeputadoEscolaridade[] = [];
  grupoSelecionado: string = '';
  filtroNome: string = '';
  carregando: boolean = false;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.carregarResumo();
  }

  carregarResumo(): void {
    this.carregando = true;
    this.apiService.getEscolaridadeResumo().subscribe({
      next: (data: any) => {
        this.resumo = Array.isArray(data) ? data : [];
        if (this.resumo.length > 0) {
          this.selecionarGrupo(this.resumo[0].grupo_escolaridade);
        } else {
          this.carregando = false;
        }
      },
      error: () => {
        this.resumo = [];
        this.carregando = false;
      }
    });
  }

  selecionarGrupo(grupo: string): void {
    this.grupoSelecionado = grupo;
    this.carregando = true;
    this.apiService.getEscolaridadeDeputados(grupo).subscribe({
      next: (data: any) => {
        this.deputados = Array.isArray(data) ? data : [];
        this.carregando = false;
      },
      error: () => {
        this.deputados = [];
        this.carregando = false;
      }
    });
  }

  get totalDeputados(): number {
    return this.resumo.reduce((acc, item) => acc + (item.total_deputados || 0), 0);
  }

  get totalGastosGeral(): number {
    return this.resumo.reduce((acc, item) => acc + (item.gasto_total || 0), 0);
  }

  get deputadosFiltrados(): DeputadoEscolaridade[] {
    if (!this.filtroNome) {
      return this.deputados;
    }
    const search = this.filtroNome.toLowerCase().trim();
    return this.deputados.filter(dep => 
      dep.nome.toLowerCase().includes(search) || 
      dep.partido.toLowerCase().includes(search) ||
      dep.uf.toLowerCase().includes(search)
    );
  }

  getPorcentagemDeputados(totalGrupo: number): number {
    const total = this.totalDeputados;
    return total > 0 ? (totalGrupo / total) * 100 : 0;
  }
}
