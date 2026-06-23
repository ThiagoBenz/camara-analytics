import {

  Component,

  OnInit

} from '@angular/core';

import {

  CommonModule

} from '@angular/common';

import {

  ApiService

} from '../../services/api.service';


@Component({

  selector: 'app-vies-politico',

  standalone: true,

  imports: [

    CommonModule

  ],

  templateUrl: './vies-politico.component.html',

  styleUrl: './vies-politico.component.css'

})

export class ViesPoliticoComponent

implements OnInit {


  aba = 'partidos';


  pesquisa = '';


  cards:any = {};


  grafico:any[] = [];


  partidos:any[] = [];


  deputados:any[] = [];


  partidosOriginais:any[] = [];


  deputadosOriginais:any[] = [];


  constructor(

    private api: ApiService

  ) {}


  ngOnInit(): void {

    this.buscarDados();

  }


  buscarDados(): void {

    this.api

      .getViesPolitico()

      .subscribe((res:any)=>{

        this.cards = res.cards;


        this.grafico = res.grafico;


        this.partidos = res.partidos;


        this.deputados = res.deputados;


        this.partidosOriginais = [

          ...res.partidos

        ];


        this.deputadosOriginais = [

          ...res.deputados

        ];

      });

  }


  filtrar(

    event:any

  ){

    const texto =

      event.target.value

      .toLowerCase()

      .trim();


    if(

      this.aba === 'partidos'

    ){

      this.partidos =

        this.partidosOriginais.filter(

          p =>

          p.partido

          .toLowerCase()

          .includes(texto)

        );

    }

    else{

      this.deputados =

        this.deputadosOriginais.filter(

          d =>

          d.nome

          .toLowerCase()

          .includes(texto)

        );

    }

  }


  trocarAba(

    aba:string

  ){

    this.aba = aba;

  }

}