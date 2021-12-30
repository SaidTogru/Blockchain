import { Component, OnInit } from '@angular/core';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  content?: string;
  blockchain?: any;
  user: string = '';
  port: number = 0;
  joined: boolean = false;

  constructor(private userService: UserService) { }

  ngOnInit(): void {
  
  }

}