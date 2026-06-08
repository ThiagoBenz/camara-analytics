import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';

import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-correlacao-fornecedor-deputado',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    MatAutocompleteModule,
    MatInputModule,
    MatFormFieldModule,
    MatIconModule
  ],
  templateUrl: './correlacao-fornecedor-deputado.component.html',
  styleUrl: './correlacao-fornecedor-deputado.component.css'
})
export class CorrelacaoFornecedorDeputadoComponent implements OnInit {

  deputados: any[] = [];
  deputadosFiltrados: any[] = [];

  deputadoSelecionado = '';

  fornecedores: any[] = [];

  totalGastos = 0;
  quantidadeFornecedores = 0;

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

    this.apiService
      .getFornecedoresDeputado(nome)
      .subscribe((data: any) => {

        this.fornecedores = data;

        this.totalGastos = this.fornecedores.reduce(
          (total: number, item: any) =>
            total + item.total_gasto,
          0
        );

        this.quantidadeFornecedores =
          this.fornecedores.length;

      });

  }

}