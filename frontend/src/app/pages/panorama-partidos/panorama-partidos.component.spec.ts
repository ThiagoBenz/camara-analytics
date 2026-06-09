import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PanoramaPartidosComponent } from './panorama-partidos.component';

describe('PanoramaPartidosComponent', () => {
  let component: PanoramaPartidosComponent;
  let fixture: ComponentFixture<PanoramaPartidosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PanoramaPartidosComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PanoramaPartidosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
