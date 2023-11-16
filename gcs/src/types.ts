export interface LocationUpdatePayload {
    type?: string;
    altitude?: number;
    rotation?: number;
    x?: number;
    y?: number;
    z?: number;
}

export interface PromethusDataType {
    status: string;
    data: {
        resultType: string;
        result: {
            metric: {
                __name__: string;
                instance: string;
                job: string;
            };
            values: [number, string][];
        }[];
    };
}