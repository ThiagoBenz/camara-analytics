import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-panorama-partidos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './panorama-partidos.component.html',
  styleUrl: './panorama-partidos.component.css'
})
export class PanoramaPartidosComponent implements OnInit {

  abaSelecionada = 'gastos';

  dadosTabela: any[] = [];

  constructor(
    private apiService: ApiService
  ) {}

  ngOnInit(): void {

    this.carregarGastos();

  }

  selecionarAba(aba: string): void {

    this.abaSelecionada = aba;

    if (aba === 'gastos') {

      this.carregarGastos();

    }

  }

  carregarGastos(): void {

    this.apiService
      .getPanoramaPartidosGastos()
      .subscribe((data: any) => {

        this.dadosTabela = data;

      });

  }

}