import { Routes } from '@angular/router';

import { RankingGastosComponent } from './pages/ranking-gastos/ranking-gastos.component';
import { CategoriasGastosComponent} from'./pages/categorias-gastos/categorias-gastos.component';
import {CorrelacaoFornecedorDeputadoComponent} from './pages/correlacao-fornecedor-deputado/correlacao-fornecedor-deputado.component';

export const routes: Routes = [

  {
    path: '',
    redirectTo: 'ranking-gastos',
    pathMatch: 'full'
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
}

];