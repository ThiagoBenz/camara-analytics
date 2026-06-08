import { Routes } from '@angular/router';

import { RankingGastosComponent } from './pages/ranking-gastos/ranking-gastos.component';
import { CategoriasGastosComponent} from'./pages/categorias-gastos/categorias-gastos.component';

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
  }

];