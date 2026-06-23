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

import {

  Chart,

  registerables

} from 'chart.js';


Chart.register(

  ...registerables

);


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


  graficoDistribuicao:any;


  graficoTemas:any;


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


        setTimeout(()=>{

          this.criarGraficos();

        },100);

      });

  }


  criarGraficos(){


    if(

      this.graficoDistribuicao

    ){

      this.graficoDistribuicao.destroy();

    }


    if(

      this.graficoTemas

    ){

      this.graficoTemas.destroy();

    }


    // ==========================

    // DISTRIBUIÇÃO IDEOLÓGICA

    // ==========================


    this.graficoDistribuicao =

    new Chart(

      'graficoDistribuicao',

      {

        type:'doughnut',

        data:{

          labels:

          this.grafico.map(

            (g:any)=>

            g.grupo

          ),

          datasets:[{

            data:

            this.grafico.map(

              (g:any)=>

              g.quantidade

            )

          }]

        },

        options:{

          responsive:true,

          maintainAspectRatio:false,

          plugins:{

            legend:{

              position:'bottom'

            }

          }

        }

      }

    );


    // ==========================

    // TEMAS PREDOMINANTES

    // ==========================


    const temas:any = {};


    this.partidos.forEach(

      (p:any)=>{


        const tema =

        p.tema_predominante;


        if(

          !tema

        ){

          return;

        }


        temas[tema] =

        (

          temas[tema]

          || 0

        )

        +

        p.total_deputados;

      }

    );


    const top10 =

      Object.entries(

        temas

      )

      .sort(

        (a:any,b:any)=>

        b[1]-a[1]

      )

      .slice(0,10);


    this.graficoTemas =

    new Chart(

      'graficoTemas',

      {

        type:'bar',

        data:{

          labels:

          top10.map(

            (t:any)=>

            t[0]

          ),

          datasets:[{

            data:

            top10.map(

              (t:any)=>

              t[1]

            )

          }]

        },

        options:{

          responsive:true,

          maintainAspectRatio:false,

          plugins:{

            legend:{

              display:false

            }

          }

        }

      }

    );

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