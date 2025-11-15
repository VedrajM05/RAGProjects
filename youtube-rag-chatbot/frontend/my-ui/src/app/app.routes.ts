import { Routes } from '@angular/router';
import {Home} from './pages/home/home'

export const routes: Routes = [
    { path:'', component:Home },
    { path: '**', redirectTo:'' } //any other URL that doesn't match above
];
