import { Component, OnInit } from '@angular/core';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-block',
  templateUrl: './block.component.html',
  styleUrls: ['./block.component.scss']
})
export class BlockComponent implements OnInit {

  content?: string;
  blockchain?: any;
  sender: string = '';
  receiver: string = '';
  amount: number = 0;

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.userService.getBlockchain().subscribe(
      data => {
        this.content = data;
        this.blockchain = JSON.parse(data).chain
        console.log(this.blockchain)
      },
      err => {
        this.content = JSON.parse(err.error).message;
      }
    );
  }

  showTransaction(index: any): void {
    console.log(index)
    console.log(this.blockchain[index].transactions)
  }

  transaction(): void {
    this.userService.makeTransaction(this.sender, this.receiver, this.amount).subscribe(
      data => {
        console.log(data)
        this.content = JSON.stringify(data)
      },
      err => {
        this.content = JSON.parse(err.error).message;
      }
    )
  }

  mine(): void {
    this.userService.mine().subscribe(
      data => {
        console.log(data)
        this.content = JSON.stringify(data)
      },
      err => {
        this.content = JSON.parse(err.error).message;
      }
    )
  }

  sync(): void {
    this.userService.sync().subscribe(
      data => {
        console.log(data)
        this.content = JSON.stringify(data)
      },
      err => {
        this.content = JSON.parse(err.error).message;
      }
    )
  }

}
