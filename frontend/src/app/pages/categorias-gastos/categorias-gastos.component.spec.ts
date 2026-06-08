import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CategoriasGastosComponent } from './categorias-gastos.component';

describe('CategoriasGastosComponent', () => {
  let component: CategoriasGastosComponent;
  let fixture: ComponentFixture<CategoriasGastosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CategoriasGastosComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CategoriasGastosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
