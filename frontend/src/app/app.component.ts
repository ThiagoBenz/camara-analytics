import { Component } from '@angular/core';

import { CommonModule } from '@angular/common';

import { RouterOutlet } from '@angular/router';

import { SidebarComponent } from './components/sidebar/sidebar.component';

import { HeaderComponent } from './components/header/header.component';


@Component({

  selector: 'app-root',

  standalone: true,

  imports: [

    CommonModule,

    RouterOutlet,

    SidebarComponent,

    HeaderComponent

  ],

  templateUrl: './app.component.html',

  styleUrl: './app.component.css'

})

export class AppComponent {

  menuAberto = true;


  toggleSidebar(): void {

    this.menuAberto = !this.menuAberto;

  }


  fecharSidebar(): void {

    this.menuAberto = false;

  }

}