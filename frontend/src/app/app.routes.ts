import { Routes } from '@angular/router';

import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { RankingGastosComponent } from './pages/ranking-gastos/ranking-gastos.component';
import { CategoriasGastosComponent } from './pages/categorias-gastos/categorias-gastos.component';
import { CorrelacaoFornecedorDeputadoComponent } from './pages/correlacao-fornecedor-deputado/correlacao-fornecedor-deputado.component';
import { PanoramaPartidosComponent } from './pages/panorama-partidos/panorama-partidos.component';

export const routes: Routes = [

  {
    path: '',
    component: DashboardComponent
  },

  {
    path: 'home',
    component: DashboardComponent
  },

  {
    path: 'ranking-gastos',
    component: RankingGastosComponent
  },

  {
    path: 'categorias-gastos',
    component: CategoriasGastosComponent
  },

  {
    path: 'correlacao-fornecedor-deputado',
    component: CorrelacaoFornecedorDeputadoComponent
  },

  {
    path: 'panorama-partidos',
    component: PanoramaPartidosComponent
  }

];