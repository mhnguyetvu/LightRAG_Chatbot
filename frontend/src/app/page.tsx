'use client';

import { useState, useRef, useEffect } from 'react';
import { chatService, QueryRequest } from '@/services/chatService';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    mode?: string;
}

const MODES = [
    { value: 'hybrid', label: 'Hybrid', desc: 'Tốt nhất' },
    { value: 'local', label: 'Local', desc: 'Cụ thể' },
    { value: 'global', label: 'Global', desc: 'Tổng quan' },
    { value: 'naive', label: 'Naive', desc: 'Đơn giản' },
];

export default function Home() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [mode, setMode] = useState<'naive' | 'local' | 'global' | 'hybrid'>('hybrid');
    const [loading, setLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, loading]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage: Message = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const request: QueryRequest = { question: input, mode };
            const response = await chatService.query(request);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: response.answer,
                mode: response.mode,
            }]);
        } catch {
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: '❌ Đã xảy ra lỗi khi xử lý câu hỏi của bạn.',
            }]);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e as any);
        }
    };

    return (
        <div className="flex flex-col h-screen bg-white">
            {/* Header */}
            <header className="flex items-center justify-between px-6 py-4 border-b border-gray-100 bg-white">
                <div className="flex items-center gap-3">
                    <div className="w-9 h-9 bg-gray-900 rounded-lg flex items-center justify-center text-white text-lg">
                        ✦
                    </div>
                    <div>
                        <h1 className="text-base font-semibold text-gray-900">LightRAG Chatbot</h1>
                        <p className="text-xs text-gray-400">Knowledge Graph Assistant</p>
                    </div>
                </div>

                {/* Mode selector */}
                <div className="flex items-center gap-1 bg-gray-100 rounded-lg p-1">
                    {MODES.map(m => (
                        <button
                            key={m.value}
                            onClick={() => setMode(m.value as any)}
                            className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${mode === m.value
                                    ? 'bg-white text-gray-900 shadow-sm'
                                    : 'text-gray-500 hover:text-gray-700'
                                }`}
                        >
                            {m.label}
                        </button>
                    ))}
                </div>
            </header>

            {/* Messages */}
            <main className="flex-1 overflow-y-auto px-4 py-6">
                <div className="max-w-3xl mx-auto space-y-6">
                    {messages.length === 0 && (
                        <div className="text-center py-24">
                            <div className="w-16 h-16 bg-gray-100 rounded-2xl flex items-center justify-center text-3xl mx-auto mb-4">
                                💬
                            </div>
                            <h2 className="text-lg font-semibold text-gray-800 mb-1">Bắt đầu trò chuyện</h2>
                            <p className="text-sm text-gray-400">Hỏi tôi bất cứ điều gì về tài liệu của bạn</p>
                            <div className="flex flex-wrap justify-center gap-2 mt-6">
                                {['Công ty tên gì?', 'Chính sách bảo hiểm?', 'Dự án Alpha là gì?'].map(q => (
                                    <button
                                        key={q}
                                        onClick={() => setInput(q)}
                                        className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-600 text-sm rounded-full transition-colors"
                                    >
                                        {q}
                                    </button>
                                ))}
                            </div>
                        </div>
                    )}

                    {messages.map((message, index) => (
                        <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                            {message.role === 'assistant' && (
                                <div className="w-7 h-7 bg-gray-900 rounded-full flex items-center justify-center text-white text-xs mr-3 mt-1 flex-shrink-0">
                                    ✦
                                </div>
                            )}
                            <div className={`max-w-[75%] ${message.role === 'user'
                                ? 'bg-gray-900 text-white rounded-2xl rounded-tr-sm px-4 py-3'
                                : 'bg-gray-50 border border-gray-100 text-gray-800 rounded-2xl rounded-tl-sm px-4 py-3'
                                }`}>
                                {message.role === 'assistant' ? (
                                    <div className="prose prose-sm max-w-none text-gray-800">
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                            {message.content}
                                        </ReactMarkdown>
                                        {message.mode && (
                                            <span className="inline-block text-xs text-gray-400 mt-1 border border-gray-200 rounded px-1.5 py-0.5">
                                                {message.mode}
                                            </span>
                                        )}
                                    </div>
                                ) : (
                                    <p className="text-sm">{message.content}</p>
                                )}
                            </div>
                        </div>
                    ))}

                    {loading && (
                        <div className="flex justify-start">
                            <div className="w-7 h-7 bg-gray-900 rounded-full flex items-center justify-center text-white text-xs mr-3 flex-shrink-0">
                                ✦
                            </div>
                            <div className="bg-gray-50 border border-gray-100 rounded-2xl rounded-tl-sm px-4 py-3">
                                <div className="flex items-center gap-1.5">
                                    <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                                    <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                                    <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>
            </main>

            {/* Input */}
            <div className="border-t border-gray-100 bg-white px-4 py-4">
                <form onSubmit={handleSubmit} className="max-w-3xl mx-auto">
                    <div className="flex items-end gap-3 bg-gray-50 border border-gray-200 rounded-2xl px-4 py-3 focus-within:border-gray-400 transition-colors">
                        <textarea
                            value={input}
                            onChange={e => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Nhập câu hỏi... (Enter để gửi, Shift+Enter xuống dòng)"
                            rows={1}
                            className="flex-1 bg-transparent text-sm text-gray-900 placeholder-gray-400 resize-none focus:outline-none max-h-32"
                            disabled={loading}
                            style={{ minHeight: '24px' }}
                        />
                        <button
                            type="submit"
                            disabled={loading || !input.trim()}
                            className="w-8 h-8 bg-gray-900 hover:bg-gray-700 disabled:bg-gray-200 text-white rounded-lg flex items-center justify-center transition-colors flex-shrink-0"
                        >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                <line x1="22" y1="2" x2="11" y2="13" />
                                <polygon points="22 2 15 22 11 13 2 9 22 2" />
                            </svg>
                        </button>
                    </div>
                    <p className="text-xs text-gray-400 text-center mt-2">
                        Mode: <span className="font-medium text-gray-600">{mode}</span> · LightRAG Knowledge Graph
                    </p>
                </form>
            </div>
        </div>
    );
}
