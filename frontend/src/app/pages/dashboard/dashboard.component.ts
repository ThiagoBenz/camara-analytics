import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {

  dashboard: any;
  destaques: any;
  fornecedoresDashboard: any;

  constructor(
    private apiService: ApiService
  ) {}

  get totalDespesasBi(): string {

    return (
      this.dashboard?.total_despesas / 1000000000
    ).toFixed(2);

  }

  formatarMilhoes(valor: number): string {

    if (!valor) return '0';

    return (valor / 1000000).toFixed(1) + ' Mi';

  }

  ngOnInit(): void {

    this.apiService
      .getDashboard()
      .subscribe((data: any) => {

        this.dashboard = data;

      });

    this.apiService
      .getDashboardDestaques()
      .subscribe((data: any) => {

        this.destaques = data;

      });

    this.apiService
      .getDashboardFornecedores()
      .subscribe((data: any) => {

        this.fornecedoresDashboard = data;

      });

  }

}