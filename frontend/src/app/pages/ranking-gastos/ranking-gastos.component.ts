import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-ranking-gastos',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './ranking-gastos.component.html',
  styleUrls: ['./ranking-gastos.component.css']
})
export class RankingGastosComponent implements OnInit {

  ranking: any[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {

    this.apiService.getRankingGastos().subscribe((data: any) => {
      console.log(data);
      this.ranking = data;
    });

  }
}