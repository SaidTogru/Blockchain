import { Component, OnInit } from '@angular/core';
import { StorageService } from '../_services/storage.service';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-transaction',
  templateUrl: './transaction.component.html',
  styleUrls: ['./transaction.component.scss']
})
export class TransactionComponent implements OnInit {

  content?: string;
  blockchain?: string;
  sender: any = '';
  receiver: string = '';
  amount: number = 0;

  constructor(private userService: UserService, private storageService: StorageService) { }

  ngOnInit(): void {
    this.sender = this.storageService.getUser()
    console.log(this.sender)
    this.userService.getBlockchain().subscribe(
      data => {
        this.blockchain = data;
      },
      err => {
        this.content = JSON.parse(err.error).message;
      }
    );
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

}
