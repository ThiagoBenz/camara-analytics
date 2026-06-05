import { Routes } from '@angular/router';

import { RankingGastosComponent } from './pages/ranking-gastos/ranking-gastos.component';

export const routes: Routes = [

  {
    path: '',
    redirectTo: 'ranking-gastos',
    pathMatch: 'full'
  },

  {
    path: 'ranking-gastos',
    component: RankingGastosComponent
  }

];