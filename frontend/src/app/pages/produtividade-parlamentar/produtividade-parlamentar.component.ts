import { Component, OnInit } from '@angular/core';

import { CommonModule } from '@angular/common';

import { FormsModule } from '@angular/forms';

import { HttpClient } from '@angular/common/http';


@Component({

  selector: 'app-produtividade-parlamentar',

  standalone: true,

  imports: [

    CommonModule,

    FormsModule

  ],

  templateUrl: './produtividade-parlamentar.component.html',

  styleUrl: './produtividade-parlamentar.component.css'

})

export class ProdutividadeParlamentarComponent implements OnInit {


  deputados: any[] = [];

  deputadosFiltrados: any[] = [];


  termoPesquisa = '';


  melhorIndice: any = {};

  maisPropositivo: any = {};

  maiorPresenca: any = {};


  private API =

  'http://127.0.0.1:8000/custo-beneficio';


  constructor(

    private http: HttpClient

  ) {}


  ngOnInit(): void {

    this.carregarDados();

  }


  carregarDados(): void {

    this.http

    .get<any[]>(this.API)

    .subscribe({

      next: (dados) => {

        this.deputados = dados;

        this.deputadosFiltrados = dados;


        this.carregarCards();

      },


      error: (erro) => {

        console.error(

          'Erro ao carregar dados:',

          erro

        );

      }

    });

  }


  carregarCards(): void {

    // Melhor custo x benefício

    this.melhorIndice =

      this.deputados[0];


    // Mais propositivo

    this.maisPropositivo =

      [...this.deputados]

      .sort(

        (a, b) =>

          b.total_proposicoes -

          a.total_proposicoes

      )[0];


    // Maior presença

    this.maiorPresenca =

      [...this.deputados]

      .sort(

        (a, b) =>

          b.presenca_relativa -

          a.presenca_relativa

      )[0];

  }


  pesquisar(): void {


    const termo =

      this.termoPesquisa

      .toLowerCase()

      .trim();


    if (!termo) {


      this.deputadosFiltrados =

        this.deputados;


      return;

    }


    this.deputadosFiltrados =

      this.deputados.filter(

        deputado =>

          deputado.nome_civil_dep

          .toLowerCase()

          .includes(termo)

      );

  }

}