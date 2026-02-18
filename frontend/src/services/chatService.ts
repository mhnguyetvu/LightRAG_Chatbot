import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface QueryRequest {
  question: string;
  mode?: 'naive' | 'local' | 'global' | 'hybrid';
}

export interface QueryResponse {
  question: string;
  answer: string;
  mode: string;
}

export interface InsertRequest {
  documents: string[];
}

export interface InsertResponse {
  status: string;
  count: number;
}

class ChatService {
  private api = axios.create({
    baseURL: `${API_BASE_URL}/api/v1/chat`,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  async query(request: QueryRequest): Promise<QueryResponse> {
    const response = await this.api.post<QueryResponse>('/query', request);
    return response.data;
  }

  async insertDocuments(request: InsertRequest): Promise<InsertResponse> {
    const response = await this.api.post<InsertResponse>('/insert', request);
    return response.data;
  }

  async healthCheck(): Promise<{ status: string; service: string }> {
    const response = await this.api.get('/health');
    return response.data;
  }
}

export const chatService = new ChatService();
