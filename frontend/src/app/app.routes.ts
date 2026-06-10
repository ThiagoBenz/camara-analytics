import { Routes } from '@angular/router';

import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { RankingGastosComponent } from './pages/ranking-gastos/ranking-gastos.component';
import { CategoriasGastosComponent } from './pages/categorias-gastos/categorias-gastos.component';
import { EixosDashboardComponent } from './pages/eixos-dashboard/eixos-dashboard.component';
import { CorrelacaoFornecedorDeputadoComponent } from './pages/correlacao-fornecedor-deputado/correlacao-fornecedor-deputado.component';
import { EscolaridadeDashboardComponent } from './pages/escolaridade-dashboard/escolaridade-dashboard.component';
import { FornecedoresRankingComponent } from './pages/fornecedores-ranking/fornecedores-ranking.component';
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
    path: 'eixos',
    component: EixosDashboardComponent
  },
  {
    path: 'correlacao-fornecedor-deputado',
    component: CorrelacaoFornecedorDeputadoComponent
  },
  {
    path: 'escolaridade',
    component: EscolaridadeDashboardComponent
  },
  {
    path: 'fornecedores',
    component: FornecedoresRankingComponent
  },
  {
    path: 'panorama-partidos',
    component: PanoramaPartidosComponent
  }
];