import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

const API_URL = 'http://localhost:5000/';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  constructor(private http: HttpClient) { }

  getBlockchain(): Observable<any> {
    return this.http.get(API_URL + 'api/get_chain', { responseType: 'text' });
  }

  mine(): Observable<any> {
    return this.http.get(API_URL + 'api/mine_block');
  }

  makeTransaction(sender: string, receiver: string, amount: number): Observable<any> {
    return this.http.post(API_URL + 'api/add_transaction', { "sender": sender, "receiver": receiver, "amount": amount })
  }

  getUserBoard(): Observable<any> {
    return this.http.get(API_URL + 'user', { responseType: 'text' });
  }

  getModeratorBoard(): Observable<any> {
    return this.http.get(API_URL + 'mod', { responseType: 'text' });
  }

  getAdminBoard(): Observable<any> {
    return this.http.get(API_URL + 'admin', { responseType: 'text' });
  }

  join(username: string, port: number): Observable<any> {
    return this.http.post(API_URL + 'api/join', { "username": username, "port": port });
  }

}