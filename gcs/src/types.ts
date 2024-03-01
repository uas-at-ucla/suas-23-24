export interface LocationUpdatePayload {
    orientation: {
        pitch?: number;
        roll?: number;
        yaw?: number;
    };
    GPS: {
        lat?: number;
        lon?: number;
        alt?: number;
    };
    altitude?: number;
    battery?: number;
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