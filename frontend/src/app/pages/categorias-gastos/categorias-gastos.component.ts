import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';

import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-categorias-gastos',
  standalone: true,
  imports: [CommonModule, FormsModule, MatAutocompleteModule, MatInputModule, MatIconModule],
  templateUrl: './categorias-gastos.component.html',
  styleUrl: './categorias-gastos.component.css'
})
export class CategoriasGastosComponent implements OnInit {

  deputados: any[] = [];
  deputadosFiltrados: any[] = [];

  deputadoSelecionado = '';


  gastos: any[] = [];
  totalGastos = 0;

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {

    this.apiService.getDeputados().subscribe((data: any) => {
      this.deputados = data;
      this.deputadosFiltrados = data;
    });

  }

  filtrarDeputados() {

    this.deputadosFiltrados = this.deputados.filter(
      (d: any) =>
        d.txNomeParlamentar
          .toLowerCase()
          .includes(this.deputadoSelecionado.toLowerCase())
    );  

  }

  selecionarDeputado(nome: string) {

    this.deputadoSelecionado = nome;
    this.totalGastos = 0;
    this.apiService
      .getGastosDeputado(nome)
      .subscribe((data: any) => {

        this.gastos = data;

        this.totalGastos = this.gastos.reduce(
          (total: number, item: any) => total + item.total_gasto,
          0
);

      });

  }
  
  carregarGastos() {

    if (!this.deputadoSelecionado) {
      return;
    }

    this.apiService
      .getGastosDeputado(this.deputadoSelecionado)
      .subscribe((data: any) => {
        this.gastos = data;
      });

  }
}