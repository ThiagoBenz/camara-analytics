import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProdutividadeParlamentarComponent } from './produtividade-parlamentar.component';

describe('ProdutividadeParlamentarComponent', () => {
  let component: ProdutividadeParlamentarComponent;
  let fixture: ComponentFixture<ProdutividadeParlamentarComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ProdutividadeParlamentarComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ProdutividadeParlamentarComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
